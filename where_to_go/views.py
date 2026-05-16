import json
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from places.models import Place
from django.shortcuts import get_object_or_404


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
        feature["properties"]["detailsUrl"] = f"/place/{place.id}/"
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
    return HttpResponse(place.title)
