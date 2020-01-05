from get_board import get_board
from make_moves import move
from word_finder import run_board
from time import time,sleep

def string_from_board(board, pos):
    return "".join([board[i][j] for i,j in pos])

def main():
    sleep(0.5)
    start = time()
    found = set()
    board, posboard = get_board()
    heap = run_board(board)
    start_solving = time()
    time_left = 85 + start - start_solving
    while time() - start_solving < time_left:
        while True:
            try:
                word = heap.pop().val[0]
            except:
                return None
            s = string_from_board(board, word)
            if s in found:
                continue
            break
        found.add(s)
        move(word, posboard)
    
if __name__ == '__main__':
    main()
