#DFS
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


def dfs(root, target):
    if not root:
        return None
    
    print(root.value, end=" ")  

    if root.value == target:
        return f"\nFound {target} using DFS"
    
    for child in root.children:
        result = dfs(child, target)
        if result and "Found" in result:
            return result
    
    return None



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

# DFS Run
print(dfs(C, "N"))


#C F L M G N 
#Found N using DFS
