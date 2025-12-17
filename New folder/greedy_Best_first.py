#Greedy Best-First Search

import heapq


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

def path_cost(path):
    total = 0
    for u, v in zip(path, path[1:]):
        total += next(c for (nbr, c) in graph[u] if nbr == v)
    return total

def greedy_best_first_search(start, goal):
    frontier = [(h[start], start)]
    seen = {start}
    came_from = {}
    expanded = 0

    while frontier:
        _, node = heapq.heappop(frontier)
        expanded += 1
        if node == goal:
            p = reconstruct(came_from, start, goal)
            return p, path_cost(p), expanded

        for nbr, _ in graph[node]:
            if nbr not in seen:
                seen.add(nbr)
                came_from[nbr] = node
                heapq.heappush(frontier, (h[nbr], nbr))
    return None, float("inf"), expanded

if __name__ == "__main__":
    path, cost, expanded = greedy_best_first_search("Arad", "Bucharest")
    print("GBFS path:", path)
    print("GBFS cost:", cost)
  
