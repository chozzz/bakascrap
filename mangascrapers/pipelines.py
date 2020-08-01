# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class MangascrapersPipeline:
    def process_item(self, item, spider):
        return item



class MangabookPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'choz',
            passwd = '123456',
            database = 'raw_mangabooks'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""CREATE TABLE (IF NOT EXISTS) raw_mangabooks (
            `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            `source` varchar(255) NOT NULL,
            `uri` varchar(255) NOT NULL,
            `name` varchar(255) NOT NULL,
            `alternative_name` varchar(255) DEFAULT NULL,
            `rating` tinyint(3) unsigned NOT NULL,
            `author` varchar(255) NOT NULL,
            `genres` varchar(255) NOT NULL,
            `type` varchar(50) NOT NULL,
            `summary` text NOT NULL,
            `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            KEY `source` (`source`),
            KEY `uri` (`uri`),
            KEY `name` (`name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 """)

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""
            INSERT INTO raw_mangabooks
                (source, uri, name, alternative_name, author, genres, type, summary)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['source'][0],
            item['uri'][0],
            item['name'][0],
            item['alternative_name'][0],
            item['author'][0],
            item['genres'][0],
            item['type'][0],
            item['summary'][0]
        ))
        self.conn.commit()
