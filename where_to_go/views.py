import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template import loader
from places.models import Place
from django.shortcuts import get_object_or_404
from django.urls import reverse


def show_map(request):
    places = Place.objects.all()
    features = []
    for place in places:
        feature = {}
        feature["type"] = "Feature"
        feature["geometry"] = {}
        feature["geometry"]["type"] = "Point"
        feature["geometry"]["coordinates"] = [place.longitude, place.latitude]
        feature["properties"] = {}
        feature["properties"]["title"] = place.title
        feature["properties"]["placeId"] = place.id
        feature["properties"]["detailsUrl"] = reverse(
            'place_detail', args=[place.id])
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    template = loader.get_template('map_temp.html')
    context = {'places_geojson': geojson_data}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    images = place.images.all().order_by('order')
    imgs_urls = []
    for image in images:
        image_url = image.image.url
        full_url = request.build_absolute_uri(image_url)
        imgs_urls.append(full_url)
    response_data = {
        "title": place.title,
        "imgs": imgs_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.longitude,
            "lat": place.latitude
        }
    }
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
