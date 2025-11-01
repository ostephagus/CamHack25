import json
import urllib.parse

import requests


def get_spell_suggest(s: str):
    resp = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/'
                        f'Compound/{urllib.parse.quote(s)}/JSON')
    resp.raise_for_status()
    j = resp.json()
    if j["total"] == 0:
        return []  # We don't get the [] in this case
    return json.dumps(j["dictionary_terms"]["compound"])


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('name', type=str)
    ns = ap.parse_args()
    print(get_spell_suggest(ns.name))


if __name__ == '__main__':
    main()
