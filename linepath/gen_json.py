from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

R = Path(__file__).parent.parent
sys.path.append(str(R))

if TYPE_CHECKING:
    from xml.etree.ElementTree import parse, Element
else:
    from lxml.etree import parse

if __name__ == '__main__':
    with open(R / 'cambridge.xml', 'rb') as f:
        t = parse(f).getroot()
    poss = []
    for i, a in enumerate(t):
        a: Element
        if a.tag == 'node':
            ref = int(a.get('id'))
            poss.append((float(a.get('lat')),
                         float(a.get('lon'))))
    with open(R / 'cambridge.json', 'w') as f:
        json.dump(poss, f)
