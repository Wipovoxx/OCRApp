import pytesseract
import pyscreenshot
from PIL import Image
from pynput import mouse
from pynput import keyboard

firstClick = list()
secondClick = list()


def screenshot():
    if len(firstClick) == 0 or len(secondClick) == 0:
        print("Please click two points on the screen to define the area for OCR.")
        return

    x1, y1 = firstClick[0]
    x2, y2 = secondClick[0]

    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)

    image = pyscreenshot.grab(bbox=(left, top, right, bottom))
    image.save("test.png")   # type: ignore
    result = pytesseract.image_to_string("test.png", lang='jpn')
    print("OCR Result:")
    print(result)

def on_click(x, y, button, pressed):
    if pressed and len(firstClick) == 0:
        firstClick.append((x, y))
        print("First coordinate set at ({0}, {1}).".format(x, y))
    if not pressed and len(secondClick) == 0:
        secondClick.append((x, y))
        print("Second coordinate set at ({0}, {1}).".format(x, y))

def on_move(x, y):
    return

def on_press(key):
    try:
        print('Key {0} pressed.'.format(key.char))
        if key.char == 's':
            screenshot()
        if key.char == 'r':
            print("Resetting click points.")
            firstClick.clear()
            secondClick.clear()
    except AttributeError:
        print('Special key {0} pressed.'.format(key))


with keyboard.Listener(on_press=on_press) as keyboardListener, mouse.Listener(on_click=on_click,on_move=on_move) as mouseListener:
    keyboardListener.join()
    mouseListener.join()
