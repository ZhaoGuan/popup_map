# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from get_inflxdb_data import get_position_data
from get_sticek_url import get_url
import json


def get_map_data():
    inflxdb_data = get_position_data()
    city_data = {}
    city_sticker = {}
    for data in inflxdb_data:
        position = json.loads(data['position'].replace("'", '"'))
        city_name = position['city_name']
        stticker_id = data['sticker_id']
        latitude = position['latitude']
        longitude = position['longitude']
        count = data['count']
        city_data.update(
            {city_name: {'sticker_id': stticker_id, 'latitude': latitude, 'longitude': longitude, 'count': count}})
        city_sticker.update({city_name: stticker_id})
    print(city_sticker)
    city_url = get_url(city_sticker)
    # print(city_data)
    # print(city_url)
    for city_, city_url_ in city_url.items():
        # print(city_)
        # print(city_url_)
        city_data[city_].update({'url': city_url_})
    return city_data


if __name__ == '__main__':
    print(get_map_data())
