#BFS
from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def bfs(root, target):
    if not root:
        return None

    queue = deque([root])
    while queue:
        current = queue.popleft()
        print(current.value, end=" ")   
        if current.value == target:
            return f"\nFound {target} using BFS"
        
        for child in current.children:
            queue.append(child)
    
    return f"\n{target} not found"



A = Node("A")
B = Node("B")
C = Node("C")
D = Node("D")
E = Node("E")
F = Node("F")
G = Node("G")
H = Node("H")
I = Node("I")
J = Node("J")
K = Node("K")
L = Node("L")
M = Node("M")
N = Node("N")
O = Node("O")

A.add_child(B)
A.add_child(C)

B.add_child(D)
B.add_child(E)

D.add_child(H)
D.add_child(I)

E.add_child(J)
E.add_child(K)

C.add_child(F)
C.add_child(G)

F.add_child(L)
F.add_child(M)

G.add_child(N)
G.add_child(O)

# BFS Run
print(bfs(A, "N"))

#A B C D E F G H I J K L M N 
#Found N using BFS