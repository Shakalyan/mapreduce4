#!/usr/bin/python
import sys
from utils import *

class AuthoritySum:
    def map():
        sum = 0
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue

            node_id, info = line.strip().split('\t')
            aut, hub, adjlist = get_aut_hub_set(info)
            sum += float(aut)**2
        
        print(f"\t{sum}")

    
    def reduce():
        sum = 0
        for line in sys.stdin:
            if len(line.strip()) == 0:
                continue

            sum += float(line.strip())
        print(sum)

if sys.argv[1] == 'map':
    AuthoritySum.map()
elif sys.argv[1] == 'reduce':
    AuthoritySum.reduce()
else:
    raise BaseException("map or reduce?")