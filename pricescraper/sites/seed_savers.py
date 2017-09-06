#!/usr/bin/env python3
'''This module contains a scraper for SeedSaversExchange.org'''
import re
import json
import urllib.request

from .base import BaseSite
from util import remove_punctuation, get_page_html


class SeedSavers(BaseSite):
    '''This class scrapes Product data from SeedSaversExchange.org'''
    ABBREVIATION = 'ss'

    ROOT_URL = 'http://www.seedsavers.org'
    SEARCH_URL = ROOT_URL + '/search?keywords={}'
    NO_RESULT_TEXT = 'No items found.'

    def _find_product_page(self, use_organic=True):
        '''Seed Savers Exchange doesn't like extra search terms,
            so for example, searching "Green Zebra Tomato" will get no results,
            even though they have a tomato named "Green Zebra". This function
            successivly strips out search terms to see if we get a match that way.

        '''

        search_terms_list = remove_punctuation(self.sese_name).split()
        while len(search_terms_list) > 0:
            search_terms = ' '.join(search_terms_list)
            search_page = self._search_site(search_terms)
            match = self._get_best_match_or_none(search_page)
            if match:
                return match

            if match is None and self.sese_organic:
                search_page = self._search_site(search_terms + "organic")
                organic_match = self._get_best_match_or_none(search_page)
                if organic_match:
                    return organic_match

            search_terms_list = search_terms_list[:-1]

        return None

    def _get_real_url(self):
        '''Generate the true URL of the product by simulating an AJAX request.

        Some product pages linked from search results do not contain data but
        instead use javascript to redirect to a page with the data. The URL to
        redirect to is determined by making an AJAX request to a backend
        script.

        '''
        ajax_path = 'app/site/hosting/scriptlet.nl?script=127&deploy=1&inam='

        item_parent = self._get_match_from_product_page(
            r'itemparent" value="(.*? TOP).*?"').replace(' ', '%20')
        ajax_url = ("{}/{}{}").format(self.ROOT_URL, ajax_path, item_parent)

        request = urllib.request.Request(
            ajax_url, headers={'User-Agent': 'Mozilla/5.0',
                               'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read().decode('utf8')
        data = json.loads(response)

        real_path = data['myurl']
        return '{}/{}/'.format(self.ROOT_URL, real_path)

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(r'class="facets-item-cell-grid-title" href="(.*?)">.*?itemprop="name">(.*?)<', search_page_html)

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page.

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'itemprop="name">(.*?)<\/h1>')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page.

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'itemprop="sku">(.*?)<\/span>')

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page.

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`

        '''
        return 'organic' in self._get_match_from_product_page(r'<title>(.*?)<\/title>')

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page.

        :returns: The Product's Price
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'data-rate=".*?">(.*?)<\/span>')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page.

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'<span>Packet (.*?)<\/span>')
