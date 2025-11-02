import json

import api_calls.compound_coords
import linepath.linepath

PLACE = 'cambridge'  # or 'cambridge'


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('name', type=str)
    ns = ap.parse_args()
    molJson = json.loads(api_calls.compound_coords.getJson(ns.name))
    # MolToGrid.MolToGrid.MolToGrid(molJson)
    linepath.linepath.run(molJson, PLACE)  # Call MolToGrid on its own


if __name__=="__main__":
    main()
