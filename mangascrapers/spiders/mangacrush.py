import re
import sys
import urllib.parse as urlparse
from ..items import MangabookItem, MangapageItem
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MangacrushSpider (CrawlSpider):
    name = 'mangacrush'
    allowed_domains = ['mangacrush.com']
    start_urls = []
    rules = []

    images_store = "/efs/mangas/en"

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'IMAGES_STORE': images_store
    }

    def __init__ (self, uri='', **kwargs):
        self.start_urls.append('https://mangacrush.com/manga/' + uri)
        self.rules.append(
            Rule(LinkExtractor(allow='https://mangacrush.com/manga/' + uri + '/.*'), callback='parse_link', follow=True)
        )
        super(MangacrushSpider, self).__init__(**kwargs)

    def parse_link (self, response):
        uri = urlparse.urlparse(response.url).path

        m1 = re.match(r"^/manga/([^/]+)/?$", uri)
        m2 = re.match(r"^/manga/([^/]+)/([^/]+)/?$", uri)

        if m1:
            # Mangabook
            yield self.parse_mangabook(m1, response)

        elif m2:
            # Mangapage
            yield self.parse_mangaitem(m2, response)

    def parse_mangabook (self, matches, response):
        # Mangabook
        items = MangabookItem()
        uriname = matches.group(1)
        title = response.css('.post-title h1::text').extract_first()
        rating = response.css('.post-total-rating span.score.total_votes::text').extract_first()
        author = response.css('.post-content_item .summary-content .author-content > a::text').extract_first()
        genres = response.css('.post-content_item .summary-content .genres-content a::text').extract()
        booktype = ''
        summary = response.css('.description-summary .summary__content > p:first-child::text').extract_first()
        thumbnail = response.css('.summary_image >a > img::attr(src)').extract_first()

        items['source'] = self.name
        items['uri'] = uriname
        items['name'] = title.strip()
        items['rating'] = float(rating)
        items['author'] = author.strip()
        items['genres'] = ','.join(genres)
        items['booktype'] = booktype
        items['summary'] = summary.replace('\n', ' ').replace('\r', '')
        items['thumbnail'] = thumbnail

        return items

    def parse_mangaitem (self, matches, response):
        # Mangapage
        items = MangapageItem()
        uriname = matches.group(1)
        pagename = matches.group(2)
        imageList = response.css('.reading-content div.page-break > img::attr(src)').extract()

        if imageList is not None:
            items['source'] = self.name
            items['uri'] = uriname
            items['page'] = pagename
            items['imageDirectory'] = self.images_store + '/' + uriname + '/' + pagename
            items['imageList'] = list( map((lambda x: x.strip('\n')), imageList))

        return items