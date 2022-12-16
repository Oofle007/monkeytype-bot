import numpy as nm
import time
from time import perf_counter
import pytesseract
from pynput.keyboard import Controller

keyboard = Controller()
import random

# importing OpenCV
import cv2

from PIL import ImageGrab

LENGTH_TEST_SECONDS = 15

def imToString():
    # Path of tesseract executable
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
    # ImageGrab-To capture the screen image in a loop.
    # Bbox used to capture a specific area.

    cap = ImageGrab.grab(bbox=(20, 436, 1416, 534))
    cap.save('/Users/agraddyjr/PycharmProjects/monkeytype-bot/last-screen.png')
    # cap = Image.open('/Users/agraddyjr/PycharmProjects/monkeytype-bot/sample-screen.png')
    # Converted the image to monochrome for it to be easily
    # read by the OCR and obtained the output String.
    return pytesseract.image_to_string(
        cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
        lang='eng').replace('\n', ' ').lower()


# Time to sleep to get over to tab
time.sleep(3)


def send_to_screen(character):
    keyboard.press(character)
    keyboard.release(character)


def simulate_game(characters_to_type, acc):
    time.sleep(1.5)
    characters_to_type = round(characters_to_type)
    print(characters_to_type)
    print(wpm)
    all_characters = [*imToString()]
    keys_pressed = 0
    no_incorrect_letters = round(characters_to_type * ((100-acc)*.01))
    indexes_to_miss = []
    end = 0
    starting_time = 0
    for _ in range(no_incorrect_letters):
        indexes_to_miss.append(random.randint(0, len(all_characters)-1))
        if all_characters[indexes_to_miss[-1]] == " ":
            indexes_to_miss.append(indexes_to_miss[-1] + 1)
            del indexes_to_miss[-2]
    current_index = 0
    for i in range(characters_to_type):  # Typing the entire line
        time_to_subtract = end - starting_time
        sleep_time = (LENGTH_TEST_SECONDS / characters_to_type) - time_to_subtract
        print('time_to_subtract for {}'.format(time_to_subtract))
        print('sleeping for {}'.format(sleep_time))
        time.sleep(sleep_time)  # time_each_press - (time_each_press_start - time.time()
        print('start=' + str(starting_time))
        starting_time = perf_counter()
        character = all_characters[i]
        if keys_pressed == characters_to_type:
            break
        random_no = random.randint(0, 99)
        if current_index in indexes_to_miss:
            send_to_screen('a')
        else:
            send_to_screen(character)
        # if random_no > 99:
            #keyboard.press(Key.tab)
            #break
        current_index += 1
        keys_pressed += 1
        end = perf_counter()

    time.sleep(random.randint(0, 2))
    #keyboard.press(Key.tab)


games_to_play = 1
for _ in range(games_to_play):
    wpm = random.randint(100, 120)
    acc = random.randint(92, 100)
    simulate_game(wpm * (5 / 4), acc)
