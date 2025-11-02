from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field

import requests


def get_full_data(name: str):
    resp = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound'
                        f'/name/{name}/JSON')
    resp.raise_for_status()
    return resp.json()


@dataclass
class Atom:
    idx: int
    element: int
    x: float = float('nan')
    y: float = float('nan')
    bonds: dict[int, Bond] = field(default_factory=dict)


@dataclass
class Bond:  # (James)
    order: int  # (i.e. 1 for single, 2 for double, etc.)
    style: str = ''


def style_from_annot(annot: int):
    return {
        1: "crossed",
        2: "dashed",
        3: "wavy",
        4: "dotted",
        5: "wedge-up",
        6: "wedge-down",
        7: "arrow",
        8: "aromatic",
        9: "resonance",
        10: "bold",
        11: "fischer",
        12: "closeContact",
        255: "unknown"
    }[annot]


def get_coords(full_data: dict):
    data = full_data["PC_Compounds"][0]
    atoms = {aid: Atom(idx, element) for idx, (aid, element) in enumerate(zip(
        data["atoms"]["aid"], data["atoms"]["element"]))}
    cs = data["coords"][0]["conformers"][0]
    for aid, x, y in zip(data["coords"][0]["aid"], cs["x"], cs["y"]):
        atoms[aid].x = x
        atoms[aid].y = y
    bonds = data["bonds"]
    for aid1, aid2, order in zip(bonds["aid1"], bonds["aid2"], bonds["order"]):
        a1 = atoms[aid1]
        a2 = atoms[aid2]
        a1.bonds[a2.idx] = a2.bonds[a1.idx] = Bond(order)
    for aid1, aid2, annot in zip(cs["style"]["aid1"], cs["style"]["aid2"],
                                 cs["style"]["annotation"]):
        a1 = atoms[aid1]
        a2 = atoms[aid2]
        b = a1.bonds.setdefault(a2.idx, Bond(0))  # and should also be in a2
        b.style = style_from_annot(annot)
    return [dataclasses.asdict(d) for d in atoms.values()]


def get_data(name: str):
    return get_coords(get_full_data(name))

def getJson(name):
    return json.dumps(get_data(name))

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('name', type=str)
    ns = ap.parse_args()
    print(json.dumps(get_data(ns.name)))


if __name__ == '__main__':
    main()
