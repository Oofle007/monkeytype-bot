import numpy as nm
import time
import random
import pytesseract
from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()


# importing OpenCV
import cv2
from PIL import ImageGrab


def imToString(box):
    # Path of tesseract executable
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
    # ImageGrab-To capture the screen image in a loop.
    # Bbox used to capture a specific area.

    cap = ImageGrab.grab(bbox=box)
    cap.save('/Users/agraddyjr/PycharmProjects/monkeytype-bot/last-screen.png')
    # cap = Image.open('/Users/agraddyjr/PycharmProjects/monkeytype-bot/sample-screen.png')
    # Converted the image to monochrome for it to be easily
    # read by the OCR and obtained the output String.
    return pytesseract.image_to_string(
        cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
        lang='eng').replace('\n', ' ').lower()


# Recording
def record():
    global keys_pressed
    global delays
    keys_pressed = []
    delays = []
    global time_keypress_start
    time_keypress_start = 0
    def on_press(key):
        keys_pressed.append(key)
        global time_keypress_start
        delays.append(time.perf_counter() - time_keypress_start)
        time_keypress_start = time.perf_counter()
        if str(key) == "Key.tab":
            return False
    def on_release(key):
        pass
    with Listener (on_press=on_press, on_release=on_release) as listener:
        listener.join()
    del delays[0]


def stretch_graph():
    for i in range(0, len(delays), 2):
        delays.insert(i+1, (delays[i]+delays[i+1])/2)


def play_test(wpm, acc, test_length, ifUseGraph):
    no_characters_to_type = round(wpm / (0.8/(test_length/15)))

    no_characters_typed = 0
    all_characters_index = 0
    all_characters = imToString(box=[20, 436, 1416, 534])

    # ACC
    no_wrong_characters = round(no_characters_to_type / (acc / 100) - no_characters_to_type)
    all_characters2 = all_characters.split(" ")
    print(all_characters2)
    length_all_wrong_words = 0
    index_wrong_words = 0
    while length_all_wrong_words < no_wrong_characters:
        length_all_wrong_words += len(all_characters2[index_wrong_words])
        length_all_wrong_words += 1
        index_wrong_words += 1

    no_characters_to_type += length_all_wrong_words
    alphabet = "abcdefghijklmnopqurstuvwxyz"
    all_characters = list(all_characters)
    i = -1
    while i < no_wrong_characters:
        i += 1
        replaced_letter = alphabet[random.randint(0, len(alphabet) - 1)]
        while replaced_letter == all_characters[i]:  # Not replacing the same letter
            replaced_letter = alphabet[random.randint(0, len(alphabet) - 1)]
        if all_characters[i] == " ":  # Not changing space characters
            no_wrong_characters += 1
            no_characters_to_type += 1
            continue
        all_characters[i] = replaced_letter

    if ifUseGraph:
        while len(delays) < no_characters_to_type:
            stretch_graph()
        while len(delays) > no_characters_to_type:
            del delays[-1]
        subtract_value = (sum(delays) - test_length) / len(delays)
        for i in range(len(delays)):
            delays[i-1] -= subtract_value

    start = time.perf_counter()
    while len(all_characters) > 0 and no_characters_typed < no_characters_to_type:
        character = all_characters[all_characters_index]
        keyboard.type(character)
        no_characters_typed += 1
        all_characters_index += 1
        if all_characters_index == len(all_characters):
            keyboard.type(' ')
            time.sleep(0.1)
            all_characters = imToString(box=[10, 474, 1426, 600])
            all_characters_index = 0
            print(all_characters)

        # Sets wait time between each key pressed
        time_behind = ((time.perf_counter() - start) - test_length / no_characters_to_type * no_characters_typed)
        if ifUseGraph:
            current_time = time.perf_counter()
            while current_time + delays[no_characters_typed - 1] > time.perf_counter():
                continue
        else:
            current_time = time.perf_counter()
            while current_time + test_length / no_characters_to_type - time_behind > time.perf_counter():
                continue
        time.sleep(0.01)
    print(no_characters_typed)


# record()

time.sleep(3)

play_test(200, 100, 15, False)


