import requests
import sys
import time
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, Images


class Command(BaseCommand):
    help = 'Load place from JSON URL'

    def add_arguments(self, parser):
        parser.add_argument('url', help='URL of the JSON file')

    def download_with_retry(self, url, max_retries=3, delay=1):
        """Download URL with retries on connection errors"""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response
            except requests.exceptions.ConnectionError as e:
                self.stderr.write(self.style.WARNING(
                    f'Connection error (attempt {attempt + 1}/{max_retries}): {e}'
                ))
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise
            except requests.exceptions.HTTPError as e:
                self.stderr.write(self.style.ERROR(f'HTTP error: {e}'))
                raise
            except requests.exceptions.Timeout as e:
                self.stderr.write(self.style.WARNING(f'Timeout: {e}'))
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise

    def handle(self, *args, **options):
        url = options['url']

        try:
            response = self.download_with_retry(url)
            place_data = response.json()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to load JSON: {e}'))
            sys.exit(1)

        place, created = Place.objects.get_or_create(
            title=place_data['title'],
            defaults={
                'short_description': place_data['description_short'],
                'long_description': place_data['description_long'],
                'longitude': float(place_data['coordinates']['lng']),
                'latitude': float(place_data['coordinates']['lat']),
            }
        )

        success_count = 0
        fail_count = 0
        for img_url in place_data['imgs']:
            try:
                img_response = self.download_with_retry(img_url)
                Images.objects.create(
                    place=place,
                    image=ContentFile(
                        img_response.content,
                        name=img_url.split('/')[-1]
                    )
                )
                success_count += 1
                self.stdout.write(f'Downloaded: {img_url.split("/")[-1]}')
            except Exception as e:
                fail_count += 1
                self.stderr.write(self.style.ERROR(
                    f'Failed to load image {img_url}: {e}'
                ))
                continue
        self.stdout.write(self.style.SUCCESS(
            f'Loaded: {place.title} (images: {success_count} OK, {fail_count} failed)'
        ))
