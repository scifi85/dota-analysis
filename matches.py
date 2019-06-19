import os
from pathlib import Path
from functools import lru_cache
from typing import Set

from client import OpenDotaAPI


@lru_cache(maxsize=2048)
def get_league_dir(leagueid, name, data_dir='data/competitive', **_):
    """
    Get directory path for league, create if necessary

    Args:
        leagueid (int): league ID
        name (str): league name
        data_dir (str): directory prefix. This will be used  as base for creating sub-directories

    Returns:
        str: per-league directory path
    """
    current = os.path.dirname(__file__)
    path = Path(current) / Path(data_dir) / f'{name} - {leagueid}'
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def get_fetched_matches(dir=None) -> Set[int]:
    """
    Recursively read all fetched matches

    Args:
        dir (str): string to read from. Default is ./data/competitive

    Returns:
        set: match ids
    """
    if not dir:
        dir = os.path.join(
            os.path.dirname(__file__),
            'data/competitive'
        )
    return {int(file.strip('.json')) for *_, files in os.walk(dir) for file in files}


def pro_match_ids(api, tail=None):
    """
    Generator that yields pro match ids

    Args:
        api (OpenDotaAPI): client to use
        tail (int): match id to filter query. Useful when you know that you already have a
            big amount of ids fetched

    Yields:
        int: match id
    """
    params = {'less_than_match_id': tail} if tail else {}
    while True:
        print(f'Fetching matches from {params.get("less_than_match_id", "top")}')
        resp = api.get('/proMatches', params=params)
        for match in resp.json():
            yield int(match['match_id'])
        params['less_than_match_id'] = match['match_id']


def get_pro_matches(api, ids):
    """
    Download pro matches and put to corresponding directory

    Args:
        api (OpenDotaAPI): client to use
        ids (iterable): iterable of match ids. This should be ints
    """
    fetched = get_fetched_matches()
    print(f'Got {len(fetched)} matches already downloaded')

    for id_ in ids:
        if id_ in fetched:
            print(f'Match {id_} already downloaded, skipping')
            continue

        resp = api.get(f'/matches/{id_}')
        league = resp.json()['league']
        path = get_league_dir(**league)
        with open(os.path.join(path, f'{id_}.json'), 'w') as f:
            f.write(resp.text)
        print(f'Downloaded match {id_} of league < {league["name"]} >')
        fetched.add(int(id_))


if __name__ == '__main__':
    api = OpenDotaAPI()
    ids = pro_match_ids(api)
    get_pro_matches(api, ids)
