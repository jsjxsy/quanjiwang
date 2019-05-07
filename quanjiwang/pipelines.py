# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

from quanjiwang.items import QuanjiwangItem, ActionMovieLasted, ActionMovieRankList, MovieDownload
from scrapy import log

from scrapy.exceptions import DropItem
from scrapy.mail import MailSender

import redis

from quanjiwang.settings import IMAGES_STORE

redis_db = redis.Redis(host='127.0.0.1', port=6379, db=4)  # 连接redis，相当于MySQL的conn

redis_action_movie_data_dict = "action_movie_name"
redis_action_movie_lasted_data_dict = "action_movie_lasted_name"
redis_action_movie_rank_list_data_dict = "action_movie_rank_list_name"  # key的名字，写什么都可以，这里的key相当于字典名称，而不是key值。
redis_action_movie_download_data_dict = "action_movie_download_url"


class QuanjiwangPipeline(object):

    def __init__(self):
        self.mailer = MailSender()

        self.connect = pymysql.Connect("localhost", "root", "admin1234", "quanjiwang")
        self.cursor = self.connect.cursor()

        redis_db.flushdb()  # 删除全部key，保证key为0，不然多次运行时候hlen不等于0，刚开始这里调试的时候经常出错。

    def open_spider(self, spider):
        sql_query = "DELETE  FROM action_movie_lasted"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM comedy_movie_lasted"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM affectional_movie_lasted"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM dracula_movie_lasted"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM science_fiction_movie_lasted"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM war_movie_lasted"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM feature_movie_lasted"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM comic_movie_lasted"
        self.cursor.execute(sql_query)

        sql_query = "DELETE FROM action_movie_rank_list"
        self.cursor.execute(sql_query)
        sql_query = "DELETE FROM comedy_movie_rank_list"
        self.cursor.execute(sql_query)
        sql_query = "DELETE FROM affectional_movie_rank_list"
        self.cursor.execute(sql_query)
        sql_query = "DELETE FROM dracula_movie_rank_list"
        self.cursor.execute(sql_query)
        sql_query = "DELETE  FROM science_fiction_movie_rank_list"
        self.cursor.execute(sql_query)
        sql_query = "DELETE FROM war_movie_rank_list"
        self.cursor.execute(sql_query)
        sql_query = "DELETE FROM feature_movie_rank_list"
        self.cursor.execute(sql_query)
        sql_query = "DELETE FROM comic_movie_rank_list"
        self.cursor.execute(sql_query)
        pass

    def process_item(self, item, spider):
        try:
            if isinstance(item, QuanjiwangItem):
                print('process_item--->' + item['action_movie_image_url'])
                if redis_db.hlen(redis_action_movie_data_dict) == 0:
                    sql_query = "SELECT name FROM {}".format(item['category_prefix'])
                    self.cursor.execute(sql_query)
                    # 获取所有记录列表
                    result = self.cursor.fetchall()
                    for row in result:
                        name = row[0]
                        redis_db.hset(redis_action_movie_data_dict, name, 0)

            elif isinstance(item, MovieDownload):
                if redis_db.hlen(redis_action_movie_download_data_dict) == 0:
                    sql_query = "SELECT movie_download FROM {}_download".format(item['category_prefix'])
                    self.cursor.execute(sql_query)
                    # 获取所有记录列表
                    result = self.cursor.fetchall()
                    for row in result:
                        movie_download = row[0]
                        redis_db.hset(redis_action_movie_download_data_dict, movie_download, 0)

            if isinstance(item, QuanjiwangItem):
                if redis_db.hexists(redis_action_movie_data_dict,
                                    item[
                                        'action_movie_name']):  # 取item里的url和key里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理
                    raise DropItem("Duplicate item found: %s" % item)
                print(1)
            elif isinstance(item, ActionMovieLasted):
                print(2)
            elif isinstance(item, ActionMovieRankList):
                print(3)
            elif isinstance(item, MovieDownload):
                if redis_db.hexists(redis_action_movie_download_data_dict,
                                    item['movie_download']):  # 取item里的url和key里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理
                    raise DropItem("Duplicate item found: %s" % item)
                print(4)
            # 提交sql语句
            item.save(self.cursor)
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            print(error)
            log.msg(error, log.ERROR)
        return item

    def close_spider(self, spider):
        self.mailer.send(to=["jsjxsy@163.com"],
                         subject="scray finish",
                         body="quanjiwang project completed")
        self.cursor.close()
        self.connect.close()

    pass


class ManhuadbPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'http://www.quanji666.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        if isinstance(item, QuanjiwangItem):
            image_url = item['action_movie_image_url']
            image_url_href = item['action_movie_image_url_href']
            self.default_headers['referer'] = image_url_href
            log.msg("get_media_requests==>image_url==>" + image_url, log.INFO)
            log.msg("get_media_requests==>image_url_href==>" + image_url_href, log.INFO)
            yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        if item['action_movie_image_url']:
            image_url = item['action_movie_image_url']
            str_list = image_url.split('/')
            log.msg("path ===> " + IMAGES_STORE + str_list[-2] + '/' + str_list[-1], log.ERROR)
            path = IMAGES_STORE + str_list[-2]
            self.mkdir(path)
            log.msg(path + "=====>", log.ERROR)
            os.rename(IMAGES_STORE + image_paths[0], IMAGES_STORE + str_list[-2] + '/' + str_list[-1])
        return item

    @staticmethod
    def mkdir(path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)

            print
            path + ' 创建成功'
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print
            path + ' 目录已存在'
        pass
