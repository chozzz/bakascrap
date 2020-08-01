# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


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
            `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            UNIQUE KEY `unique_index` (`source`,`name`),
            KEY `source` (`source`),
            KEY `uri` (`uri`),
            KEY `name` (`name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1""")

    def store_db(self, item):
        self.curr.execute("""
            INSERT INTO raw_mangabooks (source, uri, name, rating, author, genres, booktype, summary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                uri = VALUES(uri),
                rating = VALUES(rating),
                author = VALUES(author),
                genres = VALUES(genres),
                booktype = VALUES(booktype),
                summary = VALUES(summary),
                last_updated = NOW()
        """, (
            item['source'],
            item['uri'],
            item['name'],
            item['rating'],
            item['author'],
            item['genres'],
            item['booktype'],
            item['summary']
        ))
        self.conn.commit()


class MangapagePipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def process_item(self, item, spider):
        if item.__class__.__name__ == "MangapageItem":
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
        self.curr.execute("""CREATE TABLE IF NOT EXISTS raw_mangapages (
            `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            `source` varchar(255) NOT NULL,
            `uri` varchar(255) NOT NULL,
            `page` varchar(255) NOT NULL,
            `images` text NOT NULL,
            `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            UNIQUE KEY `unique_index` (`source`,`uri`),
            KEY `uri` (`uri`),
            KEY `source` (`source`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 """)

    def store_db(self, item):
        self.curr.execute("""
            INSERT INTO raw_mangapages (uri, source, page, images)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                page = VALUES(page),
                images = VALUES(images),
                last_updated = NOW()
        """, (
            item['uri'],
            item['source'],
            item['page'],
            item['images']
        ))

        self.conn.commit()
