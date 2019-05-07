# -*- coding: utf-8 -*-
import scrapy
import re
from quanjiwang.items import QuanjiwangItem, ActionMovieLasted, ActionMovieRankList, MovieDownload
import logging

logger = logging.getLogger()


def parse_url_category(url):
    if "http://www.quanji666.com/Dongzuodianying/" in url:
        return "action_movie"
    elif "http://www.quanji666.com/Xijudianying/" in url:
        return "comedy_movie"
    elif "http://www.quanji666.com/Aiqingdianying/" in url:
        return "affectional_movie"
    elif "http://www.quanji666.com/Kehuandianying/" in url:
        return "science_fiction_movie"
    elif "http://www.quanji666.com/Kongbudianying/" in url:
        return "dracula_movie"
    elif "http://www.quanji666.com/Zhanzhengdianying/" in url:
        return "war_movie"
    elif "http://www.quanji666.com/Juqingdianying/" in url:
        return "feature_movie"
    elif "http://www.quanji666.com/Dongman/" in url:
        return "comic_movie"
    else:
        return ""
    pass


class QuanjiwangSpiderSpider(scrapy.Spider):
    name = 'quanjiwang_spider'
    allowed_domains = ['www.quanji666.com']
    start_urls = ['http://www.quanji666.com/']

    # website Category
    def parse(self, response):
        category_link = response.xpath("//div[@class='new_nav']/ul/li/a/@href").extract()
        for index, item_link in enumerate(category_link):
            # action movie
            if 9 > index > 0:
                print(item_link)
                logger.info(item_link)
                yield scrapy.Request(item_link, callback=self.parse_home_page)

    def parse_home_page(self, response):
        node_list = response.xpath("//div[@id='classpage2']")
        # action_movie
        for node in node_list:
            initial = node.xpath("./div/div/div/a/text()").extract()
            print(initial[0])

            sub_list = node.xpath("./div/ul/li")
            for sub_node in sub_list:
                movie_item = QuanjiwangItem()
                movie_item['category_prefix'] = parse_url_category(response.url)
                logger.info("response.url-->" + response.url)
                movie_item['action_movie_initial'] = initial[0]

                serial_number = sub_node.xpath("./span/text()").extract()
                if serial_number:
                    print(serial_number[0])
                    movie_item['action_movie_serial_number'] = serial_number[0]
                else:
                    print("serial number is null")

                # detail_link
                detail_url = sub_node.xpath("./a/@href").extract()
                if detail_url:
                    print(detail_url[0])
                    logger.info(detail_url[0])
                    yield scrapy.Request(detail_url[0], callback=lambda response,
                                                                        it=movie_item: self.parse_detail_page(response,
                                                                                                              it))
                else:
                    print("detail url is null")

        update_list = response.xpath("//div[contains(@class,'gengxin')]/ul")
        for index, update_item in enumerate(update_list):
            # action_movie_lasted:
            if index == 0:
                sub_update_list = update_item.xpath("./li")
                for sub_update_item in sub_update_list:
                    action_movie_lasted_item = ActionMovieLasted()
                    action_movie_lasted_item['category_prefix'] = parse_url_category(response.url)
                    logger.info("response.url-->" + response.url)
                    action_movie_lasted_name = sub_update_item.xpath("./a/text()").extract()
                    print(action_movie_lasted_name[0])
                    logger.info(action_movie_lasted_name[0])
                    action_movie_lasted_item['action_movie_lasted_name'] = action_movie_lasted_name[0]
                    yield action_movie_lasted_item
                    # action_movie_rank_list:
            elif index == 1:
                sub_update_list = update_item.xpath("./li")
                for sub_update_item in sub_update_list:
                    action_movie_rank_list = ActionMovieRankList()
                    action_movie_rank_list['category_prefix'] = parse_url_category(response.url)
                    logger.info("response.url-->" + response.url)
                    action_movie_rank_list_ranking = sub_update_item.xpath("./p/text()").extract()
                    print(action_movie_rank_list_ranking[0])
                    logger.info(action_movie_rank_list_ranking[0])
                    action_movie_rank_list_ranking_number = re.findall("\d+", action_movie_rank_list_ranking[0])[0]
                    logger.info(action_movie_rank_list_ranking_number)
                    action_movie_rank_list['action_movie_ranking'] = action_movie_rank_list_ranking_number

                    action_movie_rank_list_name = sub_update_item.xpath("./a/text()").extract()
                    print(action_movie_rank_list_name[0])
                    logger.info(action_movie_rank_list_name[0])
                    action_movie_rank_list['action_movie_rank_list_name'] = action_movie_rank_list_name[0]
                    yield action_movie_rank_list

    @staticmethod
    def parse_detail_page(response, movie_item):
        name = response.xpath("//div[@class='lm']/h1/a/text()").extract()
        movie_item['action_movie_name'] = name[0].strip()
        print(name[0].strip())

        image_url = response.xpath("//div[@class='haibao']/a/img/@src").extract()
        movie_item['action_movie_image_url'] = image_url[0].strip()
        print(image_url[0].strip())

        image_url_href = response.xpath("//div[@class='haibao']/a/@href").extract()
        movie_item['action_movie_image_url_href'] = image_url_href[0].strip()
        print(image_url[0].strip())

        actor = response.xpath("//div[@class='zhuyan']/ul/li/text()").extract()
        movie_item['action_movie_actor'] = actor[0].strip()
        print(actor[0].strip())

        movie_type = response.xpath("//div[@class='lm']/h1/text()").extract()
        movie_item['action_movie_type'] = movie_type[0].strip().strip(" > ")
        print(movie_type[0].strip().strip(" > "))

        time = response.xpath("//div[@class='lm']/p/text()").extract()
        movie_item['action_movie_time'] = time[0].strip()
        print(time[0].strip())

        definition = movie_type[1].strip(" > ")

        movie_item['action_movie_definition'] = definition.strip()
        print(definition.strip())

        description = response.xpath("//div[@class='pp']/text()").extract()
        if description:
            print(description[0].strip())
            movie_item['action_movie_description'] = description[0].strip()
        yield movie_item
        # # movie download
        movie_download_list = response.xpath("//div[@id='liebiao']/div[contains(@id,'jishu') or contains(@id,'bofq')]")
        type_movie_download_item = ""
        for movie_download_item in movie_download_list:
            type_movie_download = movie_download_item.xpath("./div[@id='xiazai']/text()").extract()
            if type_movie_download:
                type_movie_download_item = type_movie_download[0]
                print(type_movie_download[0])
                logger.info(type_movie_download[0])

            movie_download = movie_download_item.xpath("./div[@class='juji']/a/@href").extract()
            if movie_download:
                for movie_download_sub_item in movie_download:
                    print(movie_download_sub_item)

            movie_download_sub_list = movie_download_item.xpath("./div[@class='con4']/ul")
            if movie_download_sub_list:
                print(movie_download_sub_list)
                for movie_download_sub_item in movie_download_sub_list:
                    movie_download = movie_download_sub_item.xpath("./li")
                    print(movie_download)
                    if movie_download:
                        for movie_download_sub_sub_item in movie_download:
                            movie_download_item = MovieDownload()
                            movie_download_item['category_prefix'] = parse_url_category(response.url)
                            logger.info("response.url-->" + response.url)
                            movie_download_item['movie_download_name'] = name[0].strip()
                            movie_download_item['movie_download_type'] = type_movie_download_item.strip()
                            movie_sub_download = movie_download_sub_sub_item.xpath("./a/@href").extract()
                            if movie_sub_download:
                                print(movie_sub_download[0])
                                logger.info(movie_sub_download[0])
                                movie_download_item['movie_download'] = movie_sub_download[0].strip()
                            else:
                                movie_sub_download = movie_download_sub_sub_item.xpath("./div/input/@value").extract()
                                print(movie_sub_download[0])
                                logger.info(movie_sub_download[0])
                                movie_download_item['movie_download'] = movie_sub_download[0].strip()
                            yield movie_download_item
