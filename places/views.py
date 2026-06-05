import json

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place


def show_map(request):
    places = Place.objects.all()
    features = []
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse('place_detail', args=[place.id])
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    return render(request, 'map_temp.html', {'places_geojson': geojson_data})


def place_detail(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        pk=place_id
    )
    images = place.images.all().order_by('order')
    imgs_urls = []
    for image in images:
        image_url = image.image.url
        full_url = request.build_absolute_uri(image_url)
        imgs_urls.append(full_url)
    response_data = {
        "title": place.title,
        "imgs": imgs_urls,
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude
        }
    }
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
