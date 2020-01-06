from get_board import get_board
from make_moves import move
from word_finder import run_board
from time import time,sleep
from pynput import keyboard
import threading

control = True

def string_from_board(board, pos):
    return "".join([board[i][j][0] for i,j in pos])

def main_thread():
    global control
    sleep(0.5)
    start = time()
    found = set()
    board, posboard = get_board()
    heap = run_board(board)
    start_solving = time()
    time_left = 85 + start - start_solving
    while time() - start_solving < time_left and control:
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

def on_press(key):
    global control
    print("Done")
    control = False
    return False

def main():
    t1 = keyboard.Listener(on_press=on_press)
    t1.start()
    t2 = threading.Thread(target = main_thread)
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    main()
