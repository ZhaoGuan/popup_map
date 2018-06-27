# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from sanic import Sanic
from sanic.response import json as sanic_json
from sanic import blueprints
import json
from beaker.cache import cache_regions, cache_region
import kafka_c

cache_regions.update({
    'memory': {
        'expire': 600,
        'type': 'memory'
    }
})
popup_map = blueprints.Blueprint('map', url_prefix='/map')


@cache_region('memory')
@popup_map.route("/")
async def get_sessionId(request):
    return sanic_json({'status': 0, "data": []})


if __name__ == "__main__":
    app = Sanic()
    app.add_task(kafka_c.one_consumer())
    app.blueprint(popup_map, url_prefix='/map')
    app.run(host="0.0.0.0", port=8000)
