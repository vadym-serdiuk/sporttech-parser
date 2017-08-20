import requests
import logging

log = logging.getLogger('parser')


class Parser:
    base_url = ''

    def get_page(self, uri):
        if uri == '':
            return ''

        url = uri
        if not url.startswith('http'):
            url = self.base_url + uri
        try:
            log.debug('Fetching {}'.format(url))
            response = requests.get(url)
        except Exception as e:
            log.error(str(e))
            return ''
        return response.content.decode()
