import api_calls.compound_coords
import MolToGrid.MolToGrid

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('name', type=str)
    ns = ap.parse_args()
    molJson = api_calls.compound_coords.getJson(ns.name)
    MolToGrid.MolToGrid.MolToGrid(molJson)

if __name__=="__main__":
    main()