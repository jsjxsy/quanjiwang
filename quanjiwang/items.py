# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanjiwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # action_movie
    action_movie_initial = scrapy.Field()
    action_movie_serial_number = scrapy.Field()
    action_movie_name = scrapy.Field()
    action_movie_type = scrapy.Field()
    action_movie_image_url = scrapy.Field()
    action_movie_image_url_href = scrapy.Field()
    action_movie_actor = scrapy.Field()
    action_movie_time = scrapy.Field()
    action_movie_definition = scrapy.Field()
    action_movie_description = scrapy.Field()
    category_prefix = scrapy.Field()

    def save(self, cursor):
        sql = """INSERT INTO {}(initial, serial_number,name, image_url,
                 type, time,definition,
                 actor, description)
                 VALUES ('{}','{}','{}',
                   '{}','{}','{}',
                   '{}','{}','{}')""".format(self['category_prefix'],
                                             self['action_movie_initial'].encode('utf-8'),
                                             self['action_movie_serial_number'].encode('utf-8'),
                                             self['action_movie_name'].encode('utf-8'),
                                             self['action_movie_image_url'].encode('utf-8'),
                                             self['action_movie_type'].encode('utf-8'),
                                             self['action_movie_time'].encode('utf-8'),
                                             self['action_movie_definition'].encode('utf-8'),
                                             self['action_movie_actor'].encode('utf-8'),
                                             self['action_movie_description'].encode('utf-8')
                                             )
        print("sql--->" + sql)
        cursor.execute(sql)

    pass


class ActionMovieLasted(scrapy.Item):
    # action_movie_lasted:
    action_movie_lasted_name = scrapy.Field()
    category_prefix = scrapy.Field()

    def save(self, cursor):
        sql = """INSERT INTO {}_lasted(name)
                 VALUES ('{}')""".format(self['category_prefix'],
                                         self['action_movie_lasted_name'].encode('utf-8'))
        print("sql--->" + sql)
        cursor.execute(sql)

    pass


class ActionMovieRankList(scrapy.Item):
    # action_movie_rank_list:
    action_movie_ranking = scrapy.Field()
    action_movie_rank_list_name = scrapy.Field()
    category_prefix = scrapy.Field()

    def save(self, cursor):
        sql = """INSERT INTO {}_rank_list(name, ranking)
                 VALUES ('{}','{}')""".format(
            self['category_prefix'],
            self['action_movie_rank_list_name'].encode('utf-8'),
            self['action_movie_ranking'].encode('utf-8')
        )
        print("sql--->" + sql)
        cursor.execute(sql)

    pass


class MovieDownload(scrapy.Item):
    #  movie download:
    movie_download_name = scrapy.Field()
    movie_download_type = scrapy.Field()
    movie_download = scrapy.Field()
    category_prefix = scrapy.Field()

    def save(self, cursor):
        sql = """INSERT INTO {}_download(name, type_movie_download, movie_download)
                 VALUES ('{}','{}','{}')""".format(
            self['category_prefix'],
            self['movie_download_name'].encode('utf-8'),
            self['movie_download_type'].encode('utf-8'),
            self['movie_download'].encode('utf-8')
        )
        print("sql--->" + sql)
        cursor.execute(sql)

    pass
