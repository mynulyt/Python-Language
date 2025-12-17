#IDS
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H','I'],
    'E': ['J','K'],
    'F': ['L','M'],
    'G': ['N','O'],
    'H':[],
    'I':[],
    'J':[],
    'K':[],
    'L':[],
    'M':[],
    'N':[],
    'O':[],
    

}

goal = 'N'

def depth_limited_search(node, limit):
    print(f"Visiting: {node}")
    
    if node == goal:
        return True
    if limit == 0:
        return 'cutoff'
    
    for child in tree.get(node, []):
        result = depth_limited_search(child, limit - 1)
        if result != 'cutoff':
            return True
    return 'cutoff'


def iterative_deepening_search():
    depth = 0
    while True:
        print(f"\n Level = {depth}")
        found = depth_limited_search('A', depth)
        if found != 'cutoff':
            print(f"\n Goal found at Level: {depth}")
            return
        depth += 1


iterative_deepening_search()

