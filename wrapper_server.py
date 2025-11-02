import json

import api_calls.compound_coords
import linepath.linepath

PLACE = 'cambridge'  # or 'cambridge'


def main():
    while True:
        name = input()
        if name == '!exit':
            return
        molJson = json.loads(api_calls.compound_coords.getJson(name))
        # MolToGrid.MolToGrid.MolToGrid(molJson)
        linepath.linepath.run(molJson, PLACE)  # Call MolToGrid on its own


if __name__ == "__main__":
    main()
