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
                url = 'http://cdn.kikakeyboard.com/picture/53668905e61e94acdb9bbe1d747e874e.gif'
        id_url.update({results[nu][0]: url})
    for city, sticker_id in id_data.items():
        try:
            city_url.update({city: id_url[sticker_id]})
        except:
            city_url.update({city: None})
    cursor.close()
    return city_url


if __name__ == "__main__":
    id_data = {'123asda1311': '0009f18b-1b0e-4683-92b9-c65ceab6082c',
               '123asdasdaa131': '0000bd03-ea01-4529-81f1-90a78ce9a75b',
               '123asda13221': '00016c19-14f4-406f-b72f-afe30d86db5b'}
    print(get_url(id_data))
