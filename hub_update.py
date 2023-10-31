#!/usr/bin/python
import sys
from utils import *

class HubUpdate:
    def map():
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue
                
            node_id, info = line.strip().split('\t')
            aut, hub, in_set = get_aut_hub_set(info)

            emit(node_id, info)
            for adjnode_id in in_set:
                hub_info = f"{node_id} {aut}"
                emit(adjnode_id, hub_info)


    def reduce():
        node_id = None
        node_info = None
        new_hub = 0
        out_set = []
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue

            id, info = line.strip().split('\t')

            if node_id == None:
                node_id = id
            
            if id != node_id:
                aut, hub, in_set = get_aut_hub_set(node_info)
                new_node_info = f"{aut} {new_hub} {out_set}"
                emit(node_id, new_node_info)
                new_hub = 0
                node_id = id
                out_set.clear()

            if is_node(info):
                node_id = id
                node_info = info
            else:
                out_node_id, aut = info.split(' ')
                new_hub += float(aut)
                out_set.append(int(out_node_id))
        
        aut, hub, adjlist = get_aut_hub_set(node_info)
        new_node_info = f"{aut} {new_hub} {out_set}"
        emit(node_id, new_node_info)


if sys.argv[1] == 'map':
    HubUpdate.map()
elif sys.argv[1] == 'reduce':
    HubUpdate.reduce()
else:
    raise BaseException("map, combine or reduce?")