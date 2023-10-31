#!/usr/bin/python
import sys
from utils import *

class AuthorityUpdate:
    def map():
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue
                
            node_id, info = line.strip().split('\t')
            aut, hub, out_set = get_aut_hub_set(info)

            emit(node_id, info)
            for adjnode_id in out_set:
                hub_info = f"{node_id} {hub}"
                emit(adjnode_id, hub_info)


    def reduce():
        node_id = None
        node_info = None
        new_aut = 0
        in_set = []
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue

            id, info = line.strip().split('\t')

            if node_id == None:
                node_id = id
            
            if id != node_id:
                aut, hub, out_set = get_aut_hub_set(node_info)
                new_node_info = f"{new_aut} {hub} {in_set}"
                emit(node_id, new_node_info)
                new_aut = 0
                node_id = id
                in_set.clear()

            if is_node(info):
                node_id = id
                node_info = info
            else:
                in_node_id, hub = info.split(' ')
                new_aut += float(hub)
                in_set.append(int(in_node_id))
        
        aut, hub, out_set = get_aut_hub_set(node_info)
        new_node_info = f"{new_aut} {hub} {in_set}"
        emit(node_id, new_node_info)


if sys.argv[1] == 'map':
    AuthorityUpdate.map()
elif sys.argv[1] == 'reduce':
    AuthorityUpdate.reduce()
else:
    raise BaseException("map or reduce?")