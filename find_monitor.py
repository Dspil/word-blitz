from pynput import mouse

control = False
points = []

def on_click1(x, y, button, pressed):
    global control, points
    if pressed and not control:
        points.append((x,y))
        control = True
        if len(points) == 4:
            return False
    else:
        control = False
    

with mouse.Listener(on_move = None, on_click = on_click1, on_scroll = None) as listener:
    listener.join()
print("Up: {}".format(min([i[1] for i in points])))
print("Down: {}".format(max([i[1] for i in points])))
print("Left: {}".format(min([i[0] for i in points])))
print("Right: {}".format(max([i[0] for i in points])))
