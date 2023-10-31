def get_aut_hub_set(info):
    tokens = info.split(' ')
    aut = float(tokens[0])
    hub = float(tokens[1])
    adjlist = eval(' '.join(tokens[2:]))
    return aut, hub, adjlist


def emit(key, value):
    print(f"{key}\t{value}")


def is_node(info):
    return len(info.split(' ')) > 2