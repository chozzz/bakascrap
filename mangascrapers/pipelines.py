# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import re
import scrapy
import hashlib
import urllib.request


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class MangascrapersPipeline:
    def process_item(self, item, spider):
        print(":: CLASS = " + item.__class__.__name__)
        return item

class MangabookPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "MangabookItem":
            self.store_db(item)

        return item

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'choz',
            passwd = '123456',
            database = 'mangascrapers'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS raw_mangabooks (
            `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            `source` varchar(255) NOT NULL,
            `uri` varchar(255) NOT NULL,
            `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
            `rating` float(4,2) unsigned NOT NULL,
            `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
            `genres` varchar(255) NOT NULL,
            `booktype` varchar(50) NOT NULL,
            `summary` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
            `thumbnail` varchar(1000) NOT NULL,
            `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            UNIQUE KEY `unique_index` (`source`,`name`),
            KEY `source` (`source`),
            KEY `uri` (`uri`),
            KEY `name` (`name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")

    def store_db(self, item):
        self.curr.execute("""
            INSERT INTO raw_mangabooks (source, uri, name, rating, author, genres, booktype, summary, thumbnail)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                uri = VALUES(uri),
                rating = VALUES(rating),
                author = VALUES(author),
                genres = VALUES(genres),
                booktype = VALUES(booktype),
                summary = VALUES(summary),
                thumbnail = VALUES(thumbnail),
                updated_at = NOW()
        """, (
            item['source'],
            item['uri'],
            item['name'],
            item['rating'],
            item['author'],
            item['genres'],
            item['booktype'],
            item['summary'],
            item['thumbnail']
        ))
        self.conn.commit()


class MangapagePipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "MangapageItem":
            processed_images_list = self.process_image_list(item, spider)
            self.store_db(item, processed_images_list)

        return item

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'choz',
            passwd = '123456',
            database = 'mangascrapers'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS raw_mangapages (
            `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            `source` varchar(255) NOT NULL,
            `uri` varchar(255) NOT NULL,
            `page` varchar(255) NOT NULL,
            `images` text NOT NULL,
            `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            UNIQUE KEY `unique_index` (`source`,`uri`,`page`),
            KEY `page` (`page`),
            KEY `uri` (`uri`),
            KEY `source` (`source`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")

    def store_db(self, item, processed_images_list):
        strImages = ''

        if len(processed_images_list) > 1:
            strImages = ' '.join(processed_images_list).strip()

        self.curr.execute("""
            INSERT INTO raw_mangapages (uri, source, page, images)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                images = VALUES(images),
                updated_at = NOW()
        """, (
            item['uri'],
            item['source'],
            item['page'],
            strImages
        ))

        self.conn.commit()

    def process_image_list(self, item, spider):
        processed_images = []

        if 'imageList' in item and 'imageDirectory' in item:
            for idx,image_url in enumerate(item['imageList']):
                directory = item['imageDirectory']

                if not os.path.exists(directory):
                    os.makedirs(directory)

                filename, ext = os.path.splitext(image_url)
                filename = "{}/{}{}".format(directory, idx, ext)
                processed_images.append(filename)

                if not os.path.exists(filename):
                    print("Saving manga image to " + filename)

                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(image_url, filename)

        return processed_images