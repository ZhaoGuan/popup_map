# -*- coding: utf-8 -*-
# __author__ = 'Gz'
from influxdb import InfluxDBClient

client = InfluxDBClient(host='0.0.0.0', port=8086, username='root', password='root', database='popup_geohash')


def get_position_data():
    query = 'select count(sticker_id) as count,last(sticker_id) as sticker_id,last(position) as position from position_sticker group by tag_position'
    re = client.query(query)
    return list(re.get_points(measurement='position_sticker'))


if __name__ == '__main__':
    get_position_data()
