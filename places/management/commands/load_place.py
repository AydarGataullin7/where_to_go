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
        response = requests.get(url)
        data = response.json()

        place, created = Place.objects.get_or_create(
            title=data['title'],
            defaults={
                'short_description': data['description_short'],
                'long_description': data['description_long'],
                'longitude': float(data['coordinates']['lng']),
                'latitude': float(data['coordinates']['lat']),
            }

        )

        for img_url in data['imgs']:
            img_response = requests.get(img_url)
            image = Images(place=place)
            image.image.save(img_url.split(
                '/')[-1], ContentFile(img_response.content))

        self.stdout.write(self.style.SUCCESS(f'Loaded: {place.title}'))
