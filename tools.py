from prettytable import PrettyTable


def show_table(config, data):
    table = PrettyTable(['Teams'] + config['websites'])
    for team in config['teams']:
        row = [team] + [data.get(website, {}).get(team, '') for website in config['websites']]
        table.add_row(row)
    print(table)