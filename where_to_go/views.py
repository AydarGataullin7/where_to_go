import json
from django.conf import settings
from django.http import HttpResponse
from django.template import loader


def show_map(request):
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [37.62, 55.793676]
                },
                "properties": {
                    "title": "«Легенды Москвы",
                    "placeId": "moscow_legends",
                    "detailsUrl": settings.STATIC_URL + "places/moscow_legends.json"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [37.64, 55.753676]
                },
                "properties": {
                    "title": "Крыши24.рф",
                    "placeId": "roofs24",
                    "detailsUrl": settings.STATIC_URL + "places/roofs24.json"
                }
            }
        ]
    }
    template = loader.get_template('map_temp.html')
    context = {'places_geojson': geojson_data}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
