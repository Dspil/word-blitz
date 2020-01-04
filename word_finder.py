from tree_struct import *
from heapq import *

#initialize and load lexicon
lex = lexicon()
lex.load("lexicon.wb")

max_heap = heapify([])

alphabet = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω']

#board is given
board = [['N', 'K', 'K', 'J'], ['O', 'D', 'Q', 'G'], ['X', 'I', 'E', 'L'], ['U', 'T', 'S', 'Z']]

#little change

def add_coord(x):
    if x + 1 < 4:
        return x + 1
    return None


def sub_coord(x):
    if x - 1 > 0:
        return x - 1
    return None


def find_neighbors(coords):
    neighbors = []
    x = coords[0]
    y = coords[1]
    ax = add_coord(x)
    ay = add_coord(y)
    sx = sub_coord(x)
    sy = sub_coord(y)
    if(ax != None):
        neighbors.append((ax, y))
        if(ay != None):
            neighbors.append((ax, ay))
        if(sy != None):
            neighbors.append((ax, sy))
    if(ay != None):
        neighbors.append((x, ay))
        if(sx != None):
            neighbors.append((sx, ay))
    if(sx != None):
        neighbors.append((sx, y))
        if(sy != None):
            neighbors.append((sx, sy))
    if(sy != None):
        neighbors.append((x, sy))
    return neighbors


def DFS(coords, sofar, lex_tree, board):
    sofar.add(coords)
    neighbors = find_neighbors(coords)
    for n in neighbors:
        if n in sofar or board[n[0]][n[1]] not in lex_tree.neighbors.keys():
            continue
        if lex_tree.finished_word == True:
            heapq.
        DFS(n, sofar.copy(), lex_tree.neighbors[board[n[0]][n[1]]], board)

def run_board(board):
    for i in range(4):
        for j in range(4):
            DFS((i, j), [], lex.get_tree(board[i][j]))

if __name__ == "__main__":
    run_board(board)
