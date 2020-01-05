from pynput import keyboard, mouse
import time

#globals

mymouse = mouse.Controller()
mykeyboard = keyboard.Controller()
bt = 0.05

def move(m, board):
    mymouse.position = (board[m[0][0]][m[0][1]][0] , board[m[0][0]][m[0][1]][1])
    mymouse.press(mouse.Button.left)
    time.sleep(bt)
    for i,j in m[1:]:
        mymouse.position = (board[i][j][0] , board[i][j][1])
        time.sleep(bt)
    mymouse.release(mouse.Button.left)
    time.sleep(bt)
