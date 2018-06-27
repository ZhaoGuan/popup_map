# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import blueprints
import json
from beaker.cache import cache_regions, cache_region
import kafka_c
from map_data import get_map_data

cache_regions.update({
    'memory': {
        'expire': 600,
        'type': 'memory'
    }
})
popup_map = blueprints.Blueprint('map', url_prefix='/map')


# @cache_region('memory')
@popup_map.route("/")
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
    return sanic_json({'status': 0, "data": json_data})


if __name__ == "__main__":
    app = Sanic()


    async def back_task():
        await kafka_c.one_consumer()


    app.add_task(back_task())
    app.blueprint(popup_map, url_prefix='/map')
    app.run(host="0.0.0.0", port=8000)
