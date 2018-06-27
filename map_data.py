# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from get_inflxdb_data import get_position_data
from get_sticek_url import get_url
import json


def get_map_data():
    inflxdb_data = get_position_data()
    city_data = {}
    city_sticer = {}
    for data in inflxdb_data:
        position = json.loads(data['position'].replace("'", '"'))
        city_name = position['city_name']
        stticker_id = data['sticker_id']
        latitude = position['latitude']
        longitude = position['longitude']
        city_data.update({city_name: {'stticker_id': stticker_id, 'latitude': latitude, 'longitude': longitude}})
        city_sticer.update({city_name: stticker_id})
    city_url = get_url(city_sticer)
    print(city_data)
    for city_, city_url_ in city_url:
        print(city_)
        print(city_url_)
        city_data[city_].updata({'url': city_url_})
    return city_data


if __name__ == '__main__':
    print(get_map_data())
