import logging

from parsers.paddypower import PaddypowerParser
from parsers.williamhill import WilliamhillParser

log = logging.getLogger('parser')


class Parsers:
    parsers = {
        'williamhill': WilliamhillParser,
        'paddypower': PaddypowerParser,
    }

    @classmethod
    def get(cls, website):
        parser = cls.parsers.get(website)
        if parser:
            return parser

        log.warning('No parser found for site <{}>\nAvailable websites: {}'
                    .format(website, ', '.join(cls.parsers.keys())))


def parse(config):
    data = {}
    for website in config['websites']:
        parser = Parsers.get(website)
        website_data = parser().parse(config['teams'])
        if website_data:
            log.debug('{}: {}'.format(website, website_data))
            data[website] = website_data
    return data
