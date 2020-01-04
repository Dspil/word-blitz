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
mykeyboard = keyboard.Controller()

#functions
with mss.mss() as sct:
    monitor = sct.monitors[0]
    img = np.array(sct.grab(monitor))

"""
Up: 351
Down: 644
Left: 324
Right: 610
"""

def grab_word_blitz_image():
    felmonitor = dict(monitor)
    mymouse.position = (324 - 30, 351 - 30)
    felmonitor['left'] = 324
    felmonitor['top'] = 351
    felmonitor['width'] = 286
    felmonitor['height'] = 293
    with mss.mss() as sct:
        img = np.array(sct.grab(felmonitor))[:,:,1].astype(np.float32)
    print( img)
    #plt.imshow(img, cmap = 'gray')
    #plt.show()
    return img

def load_image(fname):
    return (np.dot(mpimg.imread(fname)[:,:,:3], [0.2126, 0.7152, 0.0722])).astype(np.float32)
