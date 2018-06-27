# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import json
import geoip2.database
import geohash
from kafka import KafkaConsumer
from influxdb import InfluxDBClient
import os

PATH = os.path.dirname(os.path.abspath(__file__))
consumer = KafkaConsumer('emoji_appstore', bootstrap_servers='kika-data-gimbal0.intranet.com:9092',
                         group_id='Model_DashBoard')
client = InfluxDBClient(host='0.0.0.0', port=8086, username='root', password='root', database='popup_geohash')


def ip_to_genhash(ip):
    with geoip2.database.Reader('./GeoLite2-City.mmdb') as reader:
        response = reader.city(ip)
        country = response.country.iso_code
        specific = response.subdivisions.most_specific.name
        latitude = response.location.latitude
        longitude = response.location.longitude
        city_name = response.city.name
        print(country)
        print(specific)
        print(city_name)
        g_hash = geohash.encode(latitude, longitude)
        print(g_hash)
        result = {'g_hash': g_hash, 'city_name': city_name, 'latitude': latitude, 'longitude': longitude}
    return result


def one_consumer():
    for msg in consumer:
        if '"iid":"send"' in str(msg):
            msg = str(msg).split(',,')
            ip = msg[0].split(',')[-1]
            log = '{' + str(msg[1].split(',{')[1].split('},')[0]) + '}' + '}'
            log = log.replace('\\', '')
            log = log.replace('"{', '{').replace('}"', '}')
            # print(log)
            try:
                log_json = json.loads(log)
                kb_lang = log_json['extra']['kb_lang']
                lang = log_json['extra']['lang']
                try:
                    sticker_id = log_json['extra']['sticker_id']
                except:
                    sticker_id = log_json['extra']['item_id']
                try:
                    tag = log_json['extra']['tag']
                except:
                    try:
                        tag = log_json['extra']['tags']
                    except:
                        tag = log_json['extra']['key_word']
            except:
                pass
            print(log_json)
            try:
                position = str(ip_to_genhash(ip))
                json_body = [{
                    "measurement": "position_sticker",
                    'tags': {'tag_kb_lang': kb_lang,
                             'tag_lang': lang,
                             'tag_sticker_id': sticker_id,
                             'tag_tag': tag,
                             'tag_position': position},
                    "fields": {
                        'tag': tag,
                        'sticker_id': sticker_id,
                        'lang': lang,
                        'kb_lang': kb_lang,
                        'position': position}}]
                client.create_database('popup_geohash')
                client.write_points(json_body)
            except:
                pass


if __name__ == '__main__':
    one_consumer()
