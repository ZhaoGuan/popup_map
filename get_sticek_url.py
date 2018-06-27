# -*- coding: utf-8 -*-
# __author__ = 'Gz'
import pymysql
import json

connection = pymysql.connect(host='kika-backend-sticker-mysql1.intranet.com', port=3306, user='stickeruser0',
                             password='sw3JobOT96#0', db='backend_content_sending')


def get_url(id_data):
    cursor = connection.cursor()
    sticker_ids = ''
    for city, sticker_id in id_data.items():
        sticker_ids += "'" + sticker_id + "',"
    sql_e = "SELECT id,data FROM t_resource WHERE id IN (%s)" % sticker_ids[:-1]
    cursor.execute(sql_e)
    results = cursor.fetchall()
    id_url = {}
    city_url = {}
    number = len(results)
    for nu in range(number):
        try:
            url = json.loads(results[nu][1])['gif']['url']
        except:
            try:
                url = json.loads(results[nu][1])['origin']['url']
            except:
                url = 'https://i.pximg.net/c/100x100/img-master/img/2018/06/27/16/56/14/69426267_p0_master1200.jpg'
        id_url.update({results[nu][1]: url})
    for city, sticker_id in id_data.items():
        city_url.update({city: id_url[sticker_id]})
    cursor.close()
    return city_url


if __name__ == "__main__":
    id_data = {'123asda1311': '0009f18b-1b0e-4683-92b9-c65ceab6082c',
               '123asdasdaa131': '0000bd03-ea01-4529-81f1-90a78ce9a75b',
               '123asda13221': '00016c19-14f4-406f-b72f-afe30d86db5b'}
    print(get_url(id_data))
