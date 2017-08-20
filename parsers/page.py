import re

from bs4 import BeautifulSoup
import logging

log = logging.getLogger('parser.pages')


class Page:
    page = None

    def __init__(self, content):
        self.page = BeautifulSoup(content, 'lxml')

    def get_url_by_anchor_text(self, text, attrs=None, context=None):
        if context is None:
            context = self.page
        a_el = context.find('a', text=re.compile('\s*' + text + '\s*'), attrs=attrs)
        if a_el:
            return a_el.get('href')

        log.warning('Error finding a element by text <{}>'.format(text))
        return ''
