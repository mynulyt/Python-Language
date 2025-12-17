import math

# leaf values from your tree
tree = {
    "root": ["A1", "A2", "A3"],       
    "A1": [3,12,8],                
    "A2": [2,4,6],                
    "A3": [14,5,2]                   
}

def minimax_ab(node, depth, alpha, beta, maximizingPlayer):
  
    if isinstance(node, int):
        return node

   
    children = tree[node]

    if maximizingPlayer:    
        best = -math.inf
        for child in children:
            value = minimax_ab(child, depth+1, alpha, beta, False)
            best = max(best, value)
            alpha = max(alpha, best)
            if beta <= alpha:     
                print(f"Pruned at MAX node {node}")
                break
        return best

    else:                     
        best = math.inf
        for child in children:
            value = minimax_ab(child, depth+1, alpha, beta, True)
            best = min(best, value)
            beta = min(beta, best)
            if beta <= alpha:    
                print(f"Pruned at MIN node {node}")
                break
        return best




result = minimax_ab("root", 0, -math.inf, math.inf, True)
print("Final minimax value =", result)
