#A* Search

import heapq
from math import inf

graph = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Pitesti", 97), ("Craiova", 146)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Giurgiu": [("Bucharest", 90)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Eforie": [("Hirsova", 86)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Iasi": [("Vaslui", 92), ("Neamt", 87)],
    "Neamt": [("Iasi", 87)],
}
h = {
    "Arad": 366, "Zerind": 374, "Oradea": 380, "Sibiu": 253, "Fagaras": 176,
    "Rimnicu Vilcea": 193, "Pitesti": 100, "Timisoara": 329, "Lugoj": 244,
    "Mehadia": 241, "Drobeta": 242, "Craiova": 160, "Bucharest": 0, "Giurgiu": 77,
    "Urziceni": 80, "Hirsova": 151, "Eforie": 161, "Vaslui": 199, "Iasi": 226, "Neamt": 234
}

def reconstruct(came_from, start, goal):
    cur = goal
    path = [cur]
    while cur != start:
        cur = came_from[cur]
        path.append(cur)
    return list(reversed(path))

def a_star(start, goal):
    open_heap = [(h[start], 0, start)]  
    came_from = {}
    g_best = {start: 0}
    closed = set()
    expanded = 0

    while open_heap:
        f, g, node = heapq.heappop(open_heap)
        if node in closed:
            continue
        expanded += 1
        if node == goal:
            path = reconstruct(came_from, start, goal)
            return path, g, expanded
        closed.add(node)

        for nbr, w in graph[node]:
            ng = g + w
            if ng < g_best.get(nbr, inf):
                g_best[nbr] = ng
                came_from[nbr] = node
                heapq.heappush(open_heap, (ng + h[nbr], ng, nbr))
    return None, inf, expanded

if __name__ == "__main__":
    path, cost, expanded = a_star("Arad", "Bucharest")
    print("A* path:", path)
    print("A* cost:", cost)
   
