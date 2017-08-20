import re

from parsers.page import Page
import logging

log = logging.getLogger('parser.pages')


class MainPage(Page):
    def get_sport_url(self, sport_name):
        context = self.page.find('div', attrs={'id': 'mainNavHolder'})
        return self.get_url_by_anchor_text(sport_name, context=context)


class FootballPage(Page):
    def get_url_by_league_name(self, league_name):
        return self.get_url_by_anchor_text(league_name)


class LeaguePage(Page):
    def get_group_url(self, group_name):
        context = self.page.find('div', attrs={'id': 'outright'})
        return self.get_url_by_anchor_text(group_name, context=context)


class TablePage(Page):
    def get_teams_data(self, teams):
        data = {}
        for team in teams:
            div = self.page.find('div', attrs={'class': 'eventselection'}, text=re.compile('\s*' + team + '\s*'))
            if not div:
                log.warning('No cell with team {} found'.format(team))
                continue
            value_cell = div.find_previous_sibling()
            if not value_cell:
                log.warning('No value for team {} found'.format(team))
                continue
            data[team] = value_cell.get_text().strip()

        return data
