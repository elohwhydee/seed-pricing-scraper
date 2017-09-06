#!/usr/bin/env python3
'''This module contains a scraper for HighMowingSeeds.com'''
import re

from .base import BaseSite


class HighMowing(BaseSite):
    '''This class scrapes Product data from HighMowingSeeds.com'''
    ABBREVIATION = 'hm'

    ROOT_URL = 'https://www.highmowingseeds.com'
    SEARCH_URL = ROOT_URL + '/catalogsearch/result/?q={}'
    NO_RESULT_TEXT = '0 Results found for'
    INCLUDE_CATEGORY_IN_SEARCH = True

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(
            r'product-item-link" href=".*?com(.*?)">(.*?)<\/a>',
            search_page_html)

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page.

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'itemprop="name">(.*?)<\/span>')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page.

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'itemprop="sku">(.*?)<\/div>')

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page.

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`

        '''
        return 'organic' in self.name.lower()

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page.

        :returns: The Product's Price
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'class="price">(.*?)<\/span>')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page.

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'class=""label":"([0-9].*?)"')
