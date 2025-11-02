from __future__ import annotations

import dataclasses
import itertools
import json
import math
import struct
import sys
import time
import typing
import webbrowser
from dataclasses import field
from pathlib import Path

import pqdict
from typing import TYPE_CHECKING

R = Path(__file__).parent.parent
sys.path.append(str(R))

import linepath.mgrid as mgrid


if TYPE_CHECKING:
    from xml.etree.ElementTree import parse, Element
else:
    from lxml.etree import parse

UPDATE = False

# weighting for the 'distance from straight line' part of heuristic
ALPHA_H = 2
# weighting for the 'distance to end' part of heuristic
BETA_H = 0.1
# In general, lower value encourage more exploration (0 = Dijkstra)
#  and higher values encourage immediate progress
#  towards the goal (at the cost of a possibly-not-best path)

# weighting for the 'distance from straight line' part of G-cost. Note that
# this is applied on every node so weight should be pretty low
ALPHA_G = 0.1
# weighting for the 'distance' part of G-cost
BETA_G = 1


def distance(v1: tuple[float, float], v2: tuple[float, float]):
    return math.hypot(v2[0] - v1[0], v2[1] - v1[1])


@dataclasses.dataclass
class Line:
    a: tuple[float, float]
    b: tuple[float, float]

    @property
    def dirn(self):
        return self.b[0] - self.a[0], self.b[1] - self.a[1]

    def dist(self, to: tuple[float, float]):
        return line_point_dist(self.a, self.dirn, to)

    def length(self):
        return distance(self.a, self.b)


def line_point_dist(lpos: tuple[float, float], ldir: tuple[float, float],
                    ppos: tuple[float, float]):
    dx, dy = ldir
    px, py = lpos
    x, y = ppos
    a = dy
    b = -dx
    c = - dy*px + dx*py
    return abs((a*x+b*y+c)/(math.hypot(a, b) or 0.0001))


@dataclasses.dataclass(slots=True)
class XNode:
    ref: int
    lat: float
    lon: float
    conns: set[XNode] = field(repr=False)
    gcost: float = float('inf')  # scary!
    prev: XNode | None = None

    def __hash__(self):
        return hash(self.ref)

    def __eq__(self, other):
        return self.ref == other.ref

    @property
    def pos(self):
        return self.lat, self.lon

    def set_prev_maybe(self, inst: AStar, prev: XNode):
        new_gcost = (prev.gcost + self.distance(prev) * BETA_G
                     + inst.line.dist(self.pos) * ALPHA_G)
        if new_gcost < self.gcost:
            self.gcost = new_gcost
            self.prev = prev
            return True
        return False

    # @property
    # def fcost(self):
    #     return self.hcost + self.gcost
    #
    # @property
    # def hcost(self):
    #     return INST.line.dist((self.lat, self.lon)) * 10 + distance(
    #         (self.lat, self.lon), INST.dest_pos)

    def hcosti(self, inst: AStar):
        return inst.line.dist(self.pos) * ALPHA_H + distance(
            (self.lat, self.lon), inst.dest_pos) * BETA_H

    def fcosti(self, inst: AStar):
        return self.gcost + self.hcosti(inst)
    #
    # def __lt__(self, other):
    #     return self.fcost < other.fcost
    #
    # def __gt__(self, other):
    #     return self.fcost > other.fcost
    #
    # def __le__(self, other):
    #     return self.fcost <= other.fcost
    #
    # def __ge__(self, other):
    #     return self.fcost >= other.fcost

    def reset(self):
        self.gcost = float('inf')
        self.prev = None

    def distance(self, other: XNode):
        return distance(self.pos, other.pos)

    def topickle(self):
        return self.ref, self.lat, self.lon, {n.ref for n in self.conns}


def parse_way(nodes, w: Element):
    cn: set[XNode] = set()
    ishwy = False
    for ch in w:
        if ch.tag == 'nd':
            cn.add(nodes[int(ch.get('ref'))])
        if ch.tag == 'tag' and ch.get('k') == 'highway' and ch.get('v') != 'footway':
            ishwy = True
    if ishwy:
        for n in cn:
            n.conns |= cn - {n}


class Writer:
    nalloc_tb: dict[int, int]
    f: typing.BinaryIO
    fi: int

    def __init__(self, *files: typing.BinaryIO):
        self.fs = files
        self.nd_struct = struct.Struct('<iiH')

    def write(self, nds: list[XNode]):
        self.nalloc_tb = {n.ref: idx for idx, n in enumerate(nds)}
        self.f = self.fs[0]
        self.fi = 0
        for i, n in enumerate(nds):
            self.write_node(n)
            if i > len(nds) // len(self.fs):
                self.fi = min(self.fi + 1, len(self.fs) - 1)
                self.f = self.fs[self.fi]

    def nalloc(self, n: XNode):
        return self.nalloc_tb[n.ref]

    def write_node(self, n: XNode):
        n_conn = len(n.conns)
        assert n_conn <= 65535
        self.f.write(self.nd_struct.pack(
            round(n.lat*10_000_000), round(n.lon*10_000_000), n_conn))
        self.f.write(
            struct.pack('<' + 'I'*n_conn, *map(self.nalloc, n.conns)))


class Reader:
    def __init__(self, *files: typing.BinaryIO):
        self.fs: tuple[typing.BinaryIO, ...] = files
        self.fi = 0
        self.nd_struct = struct.Struct('<iiH')

    @property
    def curr_f(self) -> typing.BinaryIO:
        return self.fs[self.fi]

    def read_spec(self, spec: struct.Struct | str):
        spec = spec if isinstance(spec, struct.Struct) else struct.Struct(spec)
        result = self.curr_f.read(spec.size)
        while len(result) < spec.size and self.fi < len(self.fs):
            self.fi += 1
            if self.fi >= len(self.fs):
                raise EOFError()
            result += self.curr_f.read(spec.size)
        return spec.unpack(result)

    def read_node(self, i: int):
        latr, lonr, n_conn = self.read_spec(self.nd_struct)
        lat = latr / 10_000_000
        lon = lonr / 10_000_000
        conns = self.read_spec('<' + 'I' * n_conn)
        return i, lat, lon, conns

    def read(self):
        connlist = []
        nodes: list[XNode] = []
        try:
            for i in itertools.count():
                i, lat, lon, conns = self.read_node(i)
                nodes.append(XNode(i, lat, lon, set()))
                connlist.append(conns)
        except EOFError:
            pass
        for n in nodes:
            n.conns |= {nodes[ref] for ref in connlist[n.ref]}
        return {n.ref: n for n in nodes}


def load_nodes(xml: str):
    extra = '' if xml == 'albuquerque.xml' else f'-{xml.removesuffix(".xml")}'
    if UPDATE:
        t0 = time.perf_counter()
        with open(R / xml, 'rb') as f:
            t = parse(f).getroot()
        nodes: dict[int, XNode] = {}
        for i, a in enumerate(t):
            a: Element
            if a.tag == 'node':
                ref = int(a.get('id'))
                nodes[ref] = XNode(ref,
                                   float(a.get('lat')),
                                   float(a.get('lon')),
                                   set())
            if a.tag == 'way':
                parse_way(nodes, a)
            if i % 100000 == 0:
                print(i)
        del t, i, a, f
        nodes = {k: n for k, n in nodes.items() if n.conns}
        t1 = time.perf_counter()
        print(t1 - t0)
        print(len(nodes))

        print('Writing...')
        t5 = time.time()
        with (open(R / f'linepath/.nodes-cache{extra}-0.bin', 'wb') as f0,
              open(R / f'linepath/.nodes-cache{extra}-1.bin', 'wb') as f1):
            Writer(f0, f1).write([*nodes.values()])
        t6 = time.time()
        print(f'Written in {t6 - t5:.2f}s')
    else:
        print('Reading Albuquerque...')
        t5 = time.time()
        with (open(R / f'linepath/.nodes-cache{extra}-0.bin', 'rb') as f0,
              open(R / f'linepath/.nodes-cache{extra}-1.bin', 'rb') as f1):
            nodes = Reader(f0, f1).read()
        t6 = time.time()
        print(f'Read in {t6 - t5:.2f}s')
    return nodes


def findnode(fns, lat: float, lon: float):
    b = None
    bd = 1e10
    for n in fns:
        cd = math.hypot(n.lat - lat, n.lon - lon)
        if b is None or cd < bd:
            bd = cd
            b = n
    print(bd)
    return b


def filternodes(nodes, line: Line):
    maxdist = max(line.length() / 4, 0.001)  # TODO adjust?
    nds = {k: n for k, n in nodes.items()
           if line.dist((n.lat, n.lon)) < maxdist}
    for n in nds.values():
        n.reset()
    return nds


@dataclasses.dataclass()
class AStar:
    def __init__(self, nodes, a: XNode, b: XNode):
        for n in nodes.values():
            n.reset()
        self.line = Line(a.pos, b.pos)
        self.start = a
        self.start.gcost = 0  # by defn.
        self.dest = b
        self.dest_pos = (self.dest.lat, self.dest.lon)
        self.open = pqdict.pqdict.minpq({self.start: self.start.fcosti(self)})
        self.closed = set()

    def run(self) -> list[XNode]:  # TODO this is slow!
        try:
            while True:
                curr: XNode = self.open.pop()
                self.closed.add(curr)
                if curr == self.dest:
                    break
                for nh in curr.conns:
                    if nh in self.closed or nh == curr:
                        continue
                    nh.set_prev_maybe(self, curr)
                    self.open[nh] = nh.fcosti(self)  # Update or add
        except pqdict.Empty:
            end = findnode(self.closed, self.dest.lat, self.dest.lon)
        else:
            end = self.dest
        path = []
        pset = set()
        while end and end not in pset:
            path.append(end)
            pset.add(end)
            end = end.prev
        return path[::-1]


def findpath(nodes, a: XNode, b: XNode):
    return AStar(nodes, a, b).run()


HTDOC = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""></script>
  <style>
    #map { height: 1000px; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    var map = L.map('map').setView([35.126086394372976, -106.5941619873047], 12);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    var pts = %(paths)s;
    var els = %(els)s;
    for (const latlngs of pts) {
      var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
      //var polyline = L.polyline([latlngs[0], latlngs.at(-1)], {color: 'blue', dashArray: '4,10'}).addTo(map);
    }
    for (const [latlng, color] of els) {
      L.circleMarker(latlng, {radius: 10, color}).addTo(map);
    }
  </script>
</body>
</html>
'''


NODE_MEM = {}


def place_to_xml(place):
    return place.lower().removeprefix('.xml') + '.xml'


def find_paths(place, data):
    paths: set[frozenset[tuple[float, float]]]
    xml = place_to_xml(place)
    if place in NODE_MEM:
        nodes = NODE_MEM[xml]
    else:
        nodes = NODE_MEM[xml] = load_nodes(xml)
    paths, ll2elem = mgrid.MolToGrid(data, is_cam=xml=='cambridge.xml')
    print('Converting nodes...')
    point_to_xnode = {}
    xn_to_elem: dict[XNode, int] = {}
    for crd in [q for w in paths for q in w]:
        if crd not in point_to_xnode:
            xnode = findnode(nodes.values(), *crd)
            point_to_xnode[crd] = xnode
            xn_to_elem[xnode] = ll2elem[crd]
    print('Finding path... 0%')
    results = []
    # TODO: replace str(...) with color
    els = [(xn.pos, str(xn_to_elem[xn])) for xn in xn_to_elem.keys()]
    for i, (st, ed) in enumerate(paths):
        path = findpath(nodes, point_to_xnode[st], point_to_xnode[ed])
        results.append(path)
        if i % 10:
            print(f'Finding path... {(i + 1) / len(paths)*100:.0f}%')
    return results, els


def run(j, place='albuquerque'):
    t3 = time.time()
    results, els = find_paths(place, j)
    hd = HTDOC % {'paths': json.dumps([[(n.lat, n.lon) for n in r] for r in results]),
                  'els': json.dumps(els)}
    with open('__result.html', 'w') as f:
        f.write(hd)
    t4 = time.time()
    print(f'Found molecule path in {t4 - t3:.2f}s')
    webbrowser.open(Path('__result.html').absolute().as_uri())
