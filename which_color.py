import mss
import numpy as np
from pynput import mouse

def on_click(x, y, b, p):
    if x < 50 and y < 50:
        return False
    if p:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
        print(img[y,x,:3])


with mouse.Listener(on_click = on_click) as l:
    l.join()

