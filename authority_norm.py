#!/usr/bin/python
import sys
from utils import *

class AuthorityNorm:
    def map(coeff):
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue

            node_id, info = line.strip().split('\t')
            aut, hub, adjlist = get_aut_hub_set(info)
            
            new_aut = aut * float(coeff)
            new_info = f"{new_aut} {hub} {adjlist}"
            emit(node_id, new_info)


AuthorityNorm.map(sys.argv[2])