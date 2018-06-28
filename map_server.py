# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import blueprints
from beaker.cache import cache_regions, cache_region
import kafka_c
from map_data import get_map_data
from sanic_cors import CORS, cross_origin

cache_regions.update({
    'memory': {
        'expire': 300,
        'type': 'memory'
    }
})
popup_map = blueprints.Blueprint('map', url_prefix='/map')


@cache_region('memory')
@popup_map.route("/data")
async def get_sessionId(request):
    data = get_map_data()
    json_data = []
    for city, city_value in data.items():
        temp = []
        temp.append(city)
        temp.append(city_value['longitude'])
        temp.append(city_value['latitude'])
        temp.append(city_value['count'])
        try:
            temp.append(city_value['url'])
        except:
            temp.append(None)
        json_data.append(temp)
    print(request.json)
    return sanic_json({'status': 0, "data": str(json_data)})


if __name__ == "__main__":
    app = Sanic()
    CORS(app)
    app.blueprint(popup_map, url_prefix='/map')
    app.run(host="0.0.0.0", port=8000)
