from get_board import get_board
from make_moves import move
from word_finder import run_board
from time import time


def main():
    start = time()
    board, posboard = get_board()
    heap = run_board(board)
    start_solving = time()
    time_left = 60 + start - start_solving
    while time() - start_solving < time_left:
        word = heap.pop()
        move(word, posboard)
    
