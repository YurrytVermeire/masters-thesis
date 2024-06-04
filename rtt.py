#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import random
import traceback
from threading import Thread

from lib.common.abstracts import Auxiliary

import pyautogui
import AppOpener

# Time to sleep between moving the mouse
MIN_MOUSE_SLEEP = 0.6
MAX_MOUSE_SLEEP = 1.5

# Time to wait before pressing the next key
MIN_KEY_SLEEP = 0.3
MAX_KEY_SLEEP = 1.0

# Amount of points to visit with the mouse movement.
MIN_POINTS = 10
MAX_POINTS = 15

log = logging.getLogger(__name__)

def random_path(min_points : int, max_points : int) -> list:
    """Generates an random sized array of points inside the display, contains no less than 10 and at max 30 points

    Parameters:
    min_points (int): Minimum amount of points to generate
    max_points (int): Maximum amount of points to generate

    Returns:
    list: an array of points
    """
    result = []
    x_max, y_max = pyautogui.size()
    array_size = random.randint(min_points, max_points)
    for point in range(0, array_size):
        x_rand = random.randint(0, x_max)
        y_rand = random.randint(0, y_max)
        random_point = (x_rand, y_rand)
        result.append(random_point)
    return result

def random_movement():
    """Gives a random pyautogui mouse movement function to use in pyautogui.moveTo

    Returns:
    function: random pyautogui mouse movement
    """
    movement_types = [pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad, pyautogui.easeInBounce, pyautogui.easeInElastic]
    random_index = random.randint(0, len(movement_types)-1)
    return movement_types[random_index]

def move_mouse(points : list, enable_clicks : bool = False) -> None:
    """Function that moves the mouse around the screen in a randomized pattern with a randomized speed.
    
    Parameters:
    points (list): array of tuples of x and y coordinates e.g. [(10,52),(555,95)]
    enable_clicks (bool or None): enable clicking between movements with a 50% chance

    Returns:
    None
    """
    filter(pyautogui.onScreen, points)
    for (x,y) in points:
        pyautogui.moveTo(x,y,random.uniform(0.5, 2), random_movement())
        if enable_clicks and (random.uniform(0,1) > 0.5):
            pyautogui.mouseDown()
            pyautogui.sleep(random.uniform(0,0.3))
            pyautogui.mouseUp()
            # chance of a double click
            if (random.uniform(0,1) > 0.5):
                pyautogui.mouseDown()
                pyautogui.sleep(random.uniform(0,0.3))
                pyautogui.mouseUp()

def random_sleep(min_sleep : float, max_sleep : float) -> None:
    """ Randomized execution sleep between an interval
    
    Parameters:
    min_sleep (int): Minimum time to sleep
    max_sleep (int): Maximum time to sleep
    """
    random_seconds = random.uniform(min_sleep, max_sleep)
    pyautogui.sleep(random_seconds)

def open_application(application_name : str):
    """ Open an application with only its name
    
    Parameters:
    application_name (str): Name of the application to open

    Returns:
    None
    """
    AppOpener.open(application_name, throw_error=False)

def close_application(application_name : str):
    """ Closes an application with only its name
    
    Parameters:
    application_name (str): Name of the application to close

    Returns:
    None
    """
    AppOpener.close(application_name, throw_error=False)

def write_on_screen(txt_array : str, azerty : bool=False) -> None:
    """ Writes a text on screen with a random delay between keypresses
    
    Parameters:
    txt_array (list): Array that contains the text needed to be typed
    azerty (bool): indicates if the keyboard layout used is AZERTY

    Returns:
    None
    """
    if azerty:
        qwerty = str.maketrans('qwazQWAZmM,?', 'azqwAZQW,?mM')
        txt_array = txt_array.translate(qwerty)

    index = 0
    for i in txt_array:
        if ((i == '\\')): 
            if (txt_array[index + 1] == 'n'):
                pyautogui.press('enter')
            elif (txt_array[index + 1] == 't'):
                pyautogui.press('tab')
            random_sleep(MIN_KEY_SLEEP,MAX_KEY_SLEEP)
        elif str.isupper(i):
            pyautogui.keyDown("shift")
            random_sleep(MIN_KEY_SLEEP, MAX_KEY_SLEEP)
            pyautogui.press(i)
            random_sleep(MIN_KEY_SLEEP, MAX_KEY_SLEEP)
            pyautogui.keyUp("shift")
        else:
            pyautogui.press(i)
            random_sleep(MIN_KEY_SLEEP,MAX_KEY_SLEEP)
        index = index + 1

class Morrigu(Auxiliary, Thread):

    def __init__(self, options, config):
        Auxiliary.__init__(self, options, config)
        Thread.__init__(self)
        self.config = config
        self.enabled = self.config.human_morrigu
        self.do_run = self.enabled

    def stop(self):
        self.do_run = False

    def run(self):
        try:
            APP = 'notepad'
            input_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit felis, efficitur a ullamcorper quis, pellentesque egestas nisl. Fusce at porta velit, et sollicitudin tortor. Cras et hendrerit odio. Duis tincidunt tellus odio, vel efficitur lectus malesuada non. Aenean elementum risus vel varius dictum. Donec placerat ultricies varius. Integer dapibus fermentum magna, vel hendrerit erat lobortis feugiat. Nunc at congue mauris, sed volutpat diam. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam rhoncus venenatis mi et varius. Nullam non tortor quis dolor lacinia finibus vitae ut mi. Donec nunc quam, ultricies in arcu nec, rhoncus rutrum turpis. 
\n Phasellus a est vel sapien varius suscipit ut a sapien. Mauris ut mi velit. Morbi porta ultrices odio, in suscipit erat aliquam at. Nam in diam nisl. Sed euismod vel massa vitae aliquet. Ut pellentesque, justo eget commodo tincidunt, dolor risus pharetra lacus, at iaculis eros ante vitae massa. Vestibulum sed tellus ut nisi mattis bibendum. Praesent et magna elit. Phasellus tincidunt ut leo at tincidunt. Cras nec purus a velit tincidunt vulputate quis et lorem. Maecenas quis ex fringilla, finibus risus at, interdum augue. Donec viverra, ipsum rutrum ornare eleifend, nisl eros molestie risus, vel vulputate enim ex non dui. In iaculis iaculis mollis. In a nisl tortor. Vivamus imperdiet felis lacus.
\nNullam a urna feugiat lorem euismod mattis. Quisque tempor quam a enim laoreet rutrum. Nam non neque consequat, ullamcorper lorem a, sodales dolor. Integer id mi eget odio venenatis gravida non in sapien. Curabitur metus nunc, gravida sit amet mi sed, porta molestie enim. In quis fermentum nibh. Etiam fermentum suscipit felis sit amet dictum. Sed tempor orci ac iaculis iaculis. Fusce in risus vitae dolor venenatis tincidunt vitae nec magna. Fusce sit amet pharetra orci. Maecenas congue sem congue dolor vestibulum, dignissim efficitur massa gravida.
\nDonec et nibh urna. Mauris sit amet sem erat. Phasellus at est vel lorem aliquet ornare. Sed id tempor enim, ullamcorper ornare lorem. Cras ultrices purus nisi, et vestibulum lacus aliquam ut. Morbi finibus sagittis lacus, vitae egestas arcu luctus sit amet. Nam ligula velit, elementum ut vestibulum non, posuere at tortor. Mauris nec nibh eleifend, finibus augue id, molestie libero. Curabitur sit amet justo ipsum. Aenean id maximus purus, in varius nunc. Sed auctor commodo nunc sollicitudin mollis. Mauris in urna in risus eleifend mollis eget in nisl. Mauris magna tortor, viverra et dolor sodales, blandit sollicitudin dolor.
\nAenean eu est maximus, interdum ante quis, tempus augue. Vivamus vehicula lacinia porta. Vivamus tincidunt vehicula ante, non sodales ex scelerisque sit amet. Aenean vestibulum ornare urna et placerat. Ut vitae pulvinar diam. Nunc in vulputate justo, et tempus velit. Nullam sed quam vel arcu fringilla bibendum. Aenean lorem nunc, mollis et pulvinar in, bibendum sed ante. "
"""

            while self.do_run:
                points = random_movement()
                move_mouse(points, enable_clicks=True)
                open_application(APP)
                write_on_screen(input_text)
                close_application(APP)
        except Exception:
            error_exc = traceback.format_exc()
            log.exception(error_exc)
