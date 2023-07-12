from pynput.keyboard import Listener

def on_press(key): # key has type "pynput...keycode"
    if key.char in "wasd":
        pass

def getListener(): 
    return Listener(on_press=on_press)