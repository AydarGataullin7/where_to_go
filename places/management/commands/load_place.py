import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, Images


class Command(BaseCommand):
    help = 'Load place from JSON URL'

    def add_arguments(self, parser):
        parser.add_argument('url', help='URL of the JSON file')

    def handle(self, *args, **options):
        url = options['url']
        try:
            response = requests.get(url)
            response.raise_for_status()
            place_data = response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to load JSON: {e}'))
            return

        place, created = Place.objects.get_or_create(
            title=place_data['title'],
            defaults={
                'short_description': place_data['description_short'],
                'long_description': place_data['description_long'],
                'longitude': float(place_data['coordinates']['lng']),
                'latitude': float(place_data['coordinates']['lat']),
            }
        )

        for img_url in place_data['imgs']:
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                image = Images(place=place)
                image.image.save(
                    img_url.split('/')[-1],
                    ContentFile(img_response.content)
                )
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(
                    f'Failed to load image {img_url}: {e}'
                ))

        self.stdout.write(self.style.SUCCESS(f'Loaded: {place.title}'))
