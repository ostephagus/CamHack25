import json

import api_calls.compound_coords
import linepath.linepath

PLACE = 'albuquerque'  # or 'cambridge'


def main():
    linepath.linepath.load_nodes(f'{PLACE}.xml')  # discard result, just cache
    while True:
        name = input()
        if name == '!exit':
            return
        molJson = json.loads(api_calls.compound_coords.getJson(name))
        # MolToGrid.MolToGrid.MolToGrid(molJson)
        linepath.linepath.run(molJson, PLACE)  # Call MolToGrid on its own


if __name__ == "__main__":
    main()
