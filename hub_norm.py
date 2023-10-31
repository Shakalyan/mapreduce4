#!/usr/bin/python
import sys
from utils import *

class HubNorm:
    def map(coeff):
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue

            node_id, info = line.strip().split('\t')
            aut, hub, adjlist = get_aut_hub_set(info)
            
            new_hub = round(hub * float(coeff), 2)
            new_info = f"{aut} {new_hub} {adjlist}"
            emit(node_id, new_info)


HubNorm.map(sys.argv[2])