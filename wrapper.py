import argparse
import json

import api_calls.compound_coords
import linepath.linepath

import cProfile

PLACE = 'albuquerque'  # or 'cambridge'


def main():
    with cProfile.Profile() as p:
        ap = argparse.ArgumentParser()
        ap.add_argument('name', type=str)
        ns = ap.parse_args()
        molJson = json.loads(api_calls.compound_coords.getJson(ns.name))
        # MolToGrid.MolToGrid.MolToGrid(molJson)
        linepath.linepath.run(molJson, PLACE)  # Call MolToGrid on its own
    p.dump_stats('p2.prof')


if __name__=="__main__":
    main()
