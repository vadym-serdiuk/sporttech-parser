import json
import logging
from argparse import ArgumentParser

import sys

import yaml

import parsers
from schedule import Schedule
from tools import show_table

console = logging.StreamHandler()
log = logging.getLogger('parser')
log.addHandler(console)
log.setLevel(logging.INFO)


class ConfigErrorException(Exception):
    pass


class CommandProcessor:
    config = {}

    def __init__(self):
        self.parser = ArgumentParser(usage='run.py <command> [options]')
        subparsers = self.parser.add_subparsers()

        schedule_parser = subparsers.add_parser('schedule', help='parse periodically and store results to a file')
        schedule_parser.set_defaults(method=self.schedule)
        self.add_global_options(schedule_parser)
        schedule_parser.add_argument('-f', '--filename', dest='filename', help='path to file with the data',
                                     required=False)

        parse_parser = subparsers.add_parser('parse', help='parse once and display results on screen')
        parse_parser.set_defaults(method=self.parse)
        self.add_global_options(parse_parser)

        show_parser = subparsers.add_parser('show', help='show the table from file')
        show_parser.set_defaults(method=self.show)
        self.add_global_options(show_parser)
        show_parser.add_argument('-f', '--filename', dest='filename', help='path to file with the data', required=False)

        args = self.parser.parse_args(sys.argv[1:])
        kwargs = vars(args)
        handler = kwargs.pop('method', None)

        debug = kwargs.pop('debug', False)
        if debug:
            log.setLevel(logging.DEBUG)

        if handler:
            config_path = kwargs.pop('config')
            try:
                self.load_config(config_path)
            except:
                return
            if self.config:
                try:
                    handler(**kwargs)
                except Exception as e:
                    log.error(str(e))
                    if debug:
                        raise

    def add_global_options(self, parser):
        parser.add_argument('-c', '--config', dest='config', help='path to config file',
                                 default='config.yaml', required=False)
        parser.add_argument('--debug', action='store_true', default=False)

    def parse(self):
        data = parsers.parse(self.config)
        show_table(self.config, data)

    def schedule(self, filename=None):
        self.config.get('schedule')[filename] = filename
        Schedule(self.config)

    def show(self, filename=None):
        if not filename:
            filename = self.config.get('schedule', {}).get('filename', 'table.json')
        with open(filename) as fp:
            data = json.load(fp)
        show_table(self.config, data)


    def load_config(self, config_path):
        errors = []
        try:
            with open(config_path) as fp:
                self.config = yaml.load(fp.read())
        except Exception as e:
            log.error(str(e))
            return

        if not 'teams' in self.config:
            errors.append('No key "teams" found in config')
        if not 'websites' in self.config:
            errors.append('No key "websites" found in config')
        if errors:
            for error in errors:
                log.error(error)
            raise ConfigErrorException()

if __name__ == '__main__':
    CommandProcessor()
