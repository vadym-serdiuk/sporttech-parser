import re

from parsers.page import Page
import logging

log = logging.getLogger('parser.pages')


class MainPage(Page):
    def get_sport_url(self, sport_name):
        context = self.page.find('div', attrs={'id': 'sitemap'})
        return self.get_url_by_anchor_text(sport_name, context=context)


class FootballPage(Page):
    def get_outrights_tab_url(self):
        context = self.page.find('div', attrs={'id': 'main'})
        return self.get_url_by_anchor_text('Outrights', context=context)


class OutrightsPage(Page):
    def get_url_by_league_name(self, league_name):
        context = self.page.find('div', attrs={'id': 'main'})
        if context:
            a_el = context.find('span', attrs={'class': 'tooltip'},
                                text=re.compile('.*' + league_name + '.*')).parent
            if a_el:
                return a_el.get('href')
        return ''


class LeaguePage(Page):
    def get_group_url(self, group_name):
        context = self.page.find('div', attrs={'class': 'outrights'})
        if context:
            a_el = context.find('span', attrs={'class': 'tooltip'},
                                text=re.compile('.*' + group_name + '.*')).parent
            if a_el:
                return a_el.get('href')
        return ''


class TablePage(Page):
    def get_teams_data(self, teams):
        data = {}
        for team in teams:
            div = self.page.find('span', attrs={'class': 'odds-label'}, text=re.compile('\s*' + team + '\s*'))
            if not div:
                log.warning('No cell with team {} found'.format(team))
                continue
            value_cell = div.find_next_sibling()
            if not value_cell:
                log.warning('No value for team {} found'.format(team))
                continue
            data[team] = value_cell.get_text().strip()

        return data
