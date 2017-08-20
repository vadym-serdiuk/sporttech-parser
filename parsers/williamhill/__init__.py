from parsers.parser import Parser
from parsers.williamhill.pages import FootballPage, LeaguePage, MainPage, TablePage


class WilliamhillParser(Parser):
    base_url = 'http://sports.williamhill.com'

    def parse(self, teams):
        main_page = MainPage(self.get_page('/'))
        football_url = main_page.get_sport_url('Football')

        if not football_url:
            return

        football_page = FootballPage(self.get_page(football_url))
        league_url = football_page.get_url_by_league_name('World Cup 2018')

        if not league_url:
            return

        league_page = LeaguePage(self.get_page(league_url))
        group_url = league_page.get_group_url(r'.*Outright')

        if not group_url:
            return

        table_page = TablePage(self.get_page(group_url))
        teams_data = table_page.get_teams_data(teams)

        return teams_data
