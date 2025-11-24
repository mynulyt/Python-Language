from collections import deque

def bfs(graph, start, goal):
    q = deque([start])
    visited = set([start])
    parent = {start: None}

    while q:
        node = q.popleft()

        if node == goal:
           
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]

        for nei in graph.get(node, []):
            if nei not in visited:
                visited.add(nei)
                parent[nei] = node
                q.append(nei)

    return None


if __name__ == "__main__":
    graph = {
        'A':['B','C'],
        'B':['D','E'],
        'C':['F'],
        'D':[],
        'E':['G'],
        'F':[],
        'G':[]
    }
    print("BFS:", bfs(graph, 'A', 'G'))
