import csv
import json
import os


def _key(player):
    score = player['benchmarks']['gold_per_min']['raw'] + player['benchmarks']['tower_damage']['raw']
    return player['isRadiant'], score


def _get_heroes(match):
    players = match['players']
    return [p['hero_id'] for p in sorted(players, key=_key, reverse=True)]


def parse_match(match):
    return _get_heroes(match), match['radiant_win']


text = []


def parse_file(file):
    global text
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
    heroes = parse_match(data)
    her = [str(el) for el in heroes[0]]
    her.append(str(int(heroes[1])))
    text.append(her)


def prepare_matches_csv():
    global text
    data_directory = os.getcwd()+'/data'
    [parse_file(dirn_name+'/'+file) for dirn_name,_,files in os.walk(data_directory) for file in files]

    header = ['r1', 'r2', 'r3', 'r4', 'r5', 'd1', 'd2', 'd3', 'd4', 'd5', 'radiant_win']
    with open('matches_new_sort.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(i for i in header)
        wr.writerows(text)
        print('DONE')


if __name__ == '__main__':
    prepare_matches_csv()