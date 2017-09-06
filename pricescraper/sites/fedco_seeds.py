#!/usr/bin/env python3
'''This module contains a scraper for FedcoSeeds.com'''
import re

from .base import BaseSite
from util import remove_punctuation, get_page_html



class FedcoSeeds(BaseSite):
    '''This class scrapes Product data from FedcoSeeds.com'''
    ABBREVIATION = 'fe'

    ROOT_URL = 'http://www.fedcoseeds.com'
    SEARCH_URL = ROOT_URL + '/seeds/search?search={}'
    SEARCH_REDIRECTED_TEXT = 'Back to Search Results'

    def _search_site(self, search_terms):
        '''Fedco wants pluses in between serach terms
        '''
        assert self.SEARCH_URL is not None
        escaped_keywords = search_terms.replace(' ', '+')
        search_url = self.SEARCH_URL.format(escaped_keywords)
        return get_page_html(search_url)

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(
            r'href="(.*?)".*?class="name".*?>(?:<span class="subcategory">)?(.*?)(?:</span>|</a>)',
            search_page_html)

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page HTML

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'Fedco Seeds - (.*?)<\/title>')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page HTML

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'"pricecell">\s(.*?):')

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page HTM

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`

        '''
        return ('<span class="og-eco" title="Certified Organic">OG</span>'
                in self.page_html)

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page HTM

        :returns: The Product's Price
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'(\$[0-9]*\.[0-9][0-9])')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page HTM

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'"pricecell">\s.*? (.*?) ')
