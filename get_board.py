import mss
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from pynput import keyboard, mouse
import os
import time
import sys

#globals

mymouse = mouse.Controller()

#functions
with mss.mss() as sct:
    monitor = sct.monitors[0]
    #img = np.array(sct.grab(monitor))


top = 351
bottom = 644
left = 324
right = 610


def grab_word_blitz_image():
    felmonitor = dict(monitor)
    mymouse.position = (left - 30, top - 30)
    felmonitor['left'] = left
    felmonitor['top'] = top
    felmonitor['width'] = right - left
    felmonitor['height'] = bottom - top
    with mss.mss() as sct:
        img = np.array(sct.grab(felmonitor))[:,:,:3].astype(np.float32)
    #imshow(img, cmap = 'gray')
    #plt.show()
    return img

def load_image(fname):
    return (np.dot(mpimg.imread(fname)[:,:,:3], [0.2126, 0.7152, 0.0722])).astype(np.float32)


def helper(img):
    return (img[60:427, 150:508] > 0.5).astype(np.uint8)

def trim(img):
    left = 0
    marker = 0
    while (img[:, left] == marker).mean() > 0.5:
        left += 1
    right = img.shape[1]
    while (img[:, right-1] == marker).mean() > 0.5:
        right -= 1
    up = 0
    while (img[up, :] == marker).mean() > 0.5:
        up += 1
    down = img.shape[0]
    while (img[down-1, :] == marker).mean() > 0.5:
        down -= 1
    return (img[up:down, left:right], up, left, down, right)


def get_letters(img):
    r = int((img.shape[0] + 0.032 * img.shape[0]) / 8)
    c = int((img.shape[1] + 0.032 * img.shape[1]) / 8)
    s = []
    for i in range(4):
        s.append([])
        for j in range(4):
            s[-1].append(img[(2 * i + 1) * r - r // 2 : (2 * i + 1) * r + r // 2, (2 * j + 1) * c - c // 2 : (2 * j + 1) * c + c // 2])
    return s

def trim_letters(s, ratio = 0.1):
    t = []
    marker = 1
    for i in s:
        t.append([])
        for j in i:
            down = j.shape[0]
            while (j[down-1, :] == marker).all():
                down -= 1
            #j = j[int(j.shape[0] * 0.1) - down:]
            up = int(j.shape[0] * 0.1)
            while (j[up, :] == marker).all():
                up += 1
            left = int(j.shape[1] * 0.1)
            while (j[:, left] == marker).all():
                left += 1
            right = int(j.shape[1] * 0.9)
            while (j[:, right-1] == marker).all():
                right -= 1
            t[-1].append(j[up:down, left:right])
    t2 = []
    marker = 0
    for i in t:
        t2.append([])
        for j in i:
            down = j.shape[0]
            while (j[down-1, :] == marker).mean() < ratio:
                down -= 1
            #j = j[int(j.shape[0] * ratio) - down:]
            up = 0
            while (j[up, :] == marker).mean() < ratio:
                up += 1
            left = 0
            while (j[:, left] == marker).mean() < ratio:
                left += 1
            right = j.shape[1]
            while (j[:, right-1] == marker).mean() < ratio:
                right -= 1
            helper = np.ones((35, 35), dtype = np.uint8)
            helper[:down-up, :right-left] = j[up:down, left:right]
            t2[-1].append(helper)
    return t2


def load_dataset():
    dataset = {}
    for i in 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ':
        os.chdir(i)
        images = os.listdir('.')
        dataset[i] = []
        for j in images:
            dataset[i].append((load_image(j) > 0.5).astype(np.float32))
        os.chdir('..')
    return dataset

def distance(img1, img2):
    return abs(img1 - img2).sum()

def which_letter(img, dataset):
    mindist = np.inf
    letter = None
    for i in 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ':
        for j in dataset[i]:
            dist = distance(img, j)
            #print dist
            if dist < mindist:
                mindist = dist
                letter = i
    return letter

def get_modifiers(colored, img):
    """
    2 words: [118, 53, 253]
    3 words: [91, 198, 254]
    2 letters: [214, 201, 126]
    3 letters: [255, 146, 194]
    """
    mods = {(118, 53, 253) : (1, 2), (91, 198, 254) : (1, 3), (214, 201, 126) : (2, 1), (255, 146, 194) : (3, 1)}
    start_cols = []
    start_rows = []
    left = 0
    up = 0
    marker = 0
    for i in range(4):
        while left < img.shape[1] and (img[:, left] == marker).mean() > 0.5:
            left += 1
        start_cols.append(left)
        while left < img.shape[1] and (img[:, left] == marker).mean() < 0.5:
            left += 1
        while up < img.shape[0] and (img[up] == marker).mean() > 0.5:
            up += 1
        start_rows.append(up)
        while up < img.shape[0] and (img[up] == marker).mean() < 0.5:
            up += 1
    modifiers = []
    for i in start_rows:
        modifiers.append([])
        for j in start_cols:
            modifiers[-1].append(mods.get(tuple(colored[i][j]), (1,1)))
    return modifiers
            

def get_board():
    bimg = grab_word_blitz_image().astype(np.uint8)
    uncolored = np.dot(bimg, [0.2126, 0.7152, 0.0722]) / 255
    img, newtop, newleft, newdown, newright = trim((uncolored > 0.5).astype(np.uint8))
    colored = bimg[newtop:newdown, newleft: newright]
    modifiers = get_modifiers(colored, img)
    newtop += top
    newleft += left
    t = [[i.astype(np.float32) for i in j] for j in trim_letters(get_letters(img))]
    data = load_dataset()
    board = []
    for i in range(4):
        board.append([])
        for j in range(4):
            board[-1].append((which_letter(t[i][j], data), modifiers[i][j][0], modifiers[i][j][1]))
    rgap = 0.033 * img.shape[0]
    cgap = 0.033 * img.shape[1]
    rlen = img.shape[0] * 0.9 / 4
    clen = img.shape[1] * 0.9 / 4
    rpos = list(map(int, [rlen / 2, rlen * 3/2 + rgap, rlen * 5/2 + 2 * rgap, rlen * 7/2 + 3 * rgap]))
    cpos = list(map(int, [clen / 2, clen * 3/2 + cgap, clen * 5/2 + 2 * cgap, clen * 7/2 + 3 * cgap]))
    posboard = [[(j + newleft, i + newtop) for j in cpos] for i in rpos]
    return board, posboard

def pb():
    x = get_board()
    for i in x:
        for j in i:
            print(j, end = " ")
        print()

def save(img, fname):
    mpimg.imsave(fname, img)

def store_letters():
    import os
    img = grab_word_blitz_image()
    t = trim_letters(get_letters(trim((img > 0.5).astype(np.uint8))))
    letters = input("Input string: ")
    for i in range(4):
        for j in range(4):
            c = letters[4 * i + j]
            name = "{}/{}.png".format(c, len(os.listdir(c)))
            save(t[i][j], name)


            
def h2(fname):
    img = load_image(fname)
    return trim_letters(get_letters(trim(helper(img))))


def store_letters2(fname):
    import os
    t = h2(fname)
    letters = input("Input string: ")
    print(letters)
    for i in range(4):
        for j in range(4):
            c = letters[4 * i + j]
            name = "{}/{}.png".format(c, len(os.listdir(c)))
            save(t[i][j], name)
            


"""
def h3(l, t):
    global s
    for i in range(4):
        for j in range(4):
            c = l[4 * i + j]
            if c not in s:
                s.add(c)
                save(t[i][j], c + ".png")
"""
def save(img, fname):
    mpimg.imsave(fname, img)

