from tree_struct import *
import heapq

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0]

    def __getitem__(self, item):
        return self.heap[item]

    def __len__(self):
        return len(self.heap)

class MaxHeap(MinHeap):
    def push(self, item):
        heapq.heappush(self.heap, Comparator(item))

class Comparator:
    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val[1] > other.val[1]

    def __eq__(self, other):
        return self.val[1] == other.val[1]

    def __repr__(self):
        return repr(self.val[0])

#initialize and load lexicon

alphabet = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Χ', 'Ψ', 'Ω']

#board is given
board = [['Ο', 'Ε', 'Ν', 'Σ'], ['Τ', 'Λ', 'Α', 'Ο'], ['Ω', 'Γ', 'Ξ', 'Ρ'], ['Μ', 'Σ', 'Ε', 'Κ']]

values = {'Α' : 1, 'Β' : 8, 'Γ' : 4, 'Δ' : 4, 'Ε' : 1, 'Ζ' : 10, 'Η' : 2, 'Θ' : 10, 'Ι' : 1, 'Κ' : 2, 'Λ' : 3, 'Μ' : 3, 'Ν' : 1, 'Ξ' : 10, 'Ο' : 1, 'Π' : 2, 'Ρ' : 2, 'Σ' : 1, 'Τ' : 1, 'Υ' : 2, 'Φ' : 8, 'Χ' : 8, 'Ψ' : 10, 'Ω' : 3}
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


def calc_points(l, board):
    sm = 0
    for i in l:
        sm += values[board[i[0]][i[1]]]
    return sm

def DFS(coords, sofar, lex_tree, board, max_heap):
    sofar.append(coords)
    neighbors = find_neighbors(coords)
    if lex_tree.finished_word == True:
        max_heap.push((sofar, calc_points(sofar, board)))
    for n in neighbors:
        if n in sofar or board[n[0]][n[1]] not in lex_tree.neighbors.keys():
            continue
        DFS(n, sofar.copy(), lex_tree.neighbors[board[n[0]][n[1]]], board, max_heap)

def run_board(board):
    lex = lexicon()
    lex.load("lexicon.wb")
    max_heap = MaxHeap()

    for i in range(4):
        for j in range(4):
            DFS((i, j), [], lex.get_tree(board[i][j]), board, max_heap)
    return max_heap

if __name__ == "__main__":
    heap = run_board(board)
    print(heap.heap[0])
