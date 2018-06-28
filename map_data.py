# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from get_inflxdb_data import get_position_data
from get_sticek_url import get_url
import json
from beaker.cache import cache_regions, cache_region

cache_regions.update({
    'memory': {
        'expire': 60,
        'type': 'memory'
    },
    'html_memory': {
        'expire': 3600,
        'type': 'memory'
    }
})


@cache_region('memory')
def get_map_data():
    inflxdb_data = get_position_data()
    city_data = {}
    city_sticker = {}
    for data in inflxdb_data:
        try:
            position = json.loads(data['position'].replace("'", '"'))
            city_name = position['city_name']
            sticker_id = data['sticker_id']
            latitude = position['latitude']
            longitude = position['longitude']
            count = data['count']
            if 'from' in sticker_id:
                pass
            else:
                city_data.update(
                    {city_name: {'sticker_id': sticker_id, 'latitude': latitude, 'longitude': longitude,
                                 'count': count}})
                city_sticker.update({city_name: sticker_id})
        except:
            pass
    city_url = get_url(city_sticker)
    # print(len(list(city_url.keys())))
    # print(len(list(city_sticker.keys())))
    # print(len(list(city_data.keys())))
    for city_, city_url_ in city_url.items():
        city_data[city_].update({'url': city_url_})
    return city_data


if __name__ == '__main__':
    print(get_map_data())
