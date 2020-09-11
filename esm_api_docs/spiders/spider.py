import urllib.parse

import scrapy
from scrapy import Request

from ..items import EsmApiDocsItem

class ESMAPIDocsSpider(scrapy.Spider):

    name = "esm_api_docs"
    allowed_domains = []

    def start_requests(self):
        yield Request( 
            url=self.url, 
            callback=self.parse_help 
        )

    def __init__(self, url):

        self.url=url
        self.allowed_domains=[urllib.parse.urlparse(url).hostname]

    def parse_help(self, response):
        """
        Arguments:  
        - response: scrapy response object for the help page
        """

        yield EsmApiDocsItem(
            url=response.url
        )

        """ Iterating through the result of get_method_list()"""
        methods = self.get_method_list(response)

        for method in methods:

            yield Request(
                url=method.xpath('@href').get(),
                callback=self.parse_method_or_type
            )
    
    def get_method_list(self, response):
        """
        Arguments:  
        - response: scrapy response object for the help page
        """
        
        return response.xpath('//div[contains(@class,"commandTitle")]/span/a')

    def parse_method_or_type(self, response):
        """
        Arguments:  
        - response: scrapy response object for the method page
        """

        yield EsmApiDocsItem(
            url=response.url
        )

        for esm_type in self.get_type_list(response):
            yield Request(
                url=esm_type.xpath('@href').get(),
                callback=self.parse_method_or_type
            )

    def get_type_list(self, response):
        """
        Arguments:  
        - response: scrapy response object for the method page
        """
        
        return [ t for t in response.xpath('//a') if '/help/types/' in t.xpath('@href').get() ] 