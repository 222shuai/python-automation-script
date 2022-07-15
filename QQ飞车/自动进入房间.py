import os
import random
import time
from threading import Thread

import pyautogui
from bdtime import tt
from pynput import keyboard
import cv2
import matplotlib
import numpy

import keyboardEmulation as ke

pyautogui.PAUSE = 1
left_right = [0x4b, 0x4d]


def go_house():
    pyautogui.moveTo(50, 80)
    pyautogui.click()
    pyautogui.moveTo(200, 80)
    pyautogui.click()
    pyautogui.moveTo(500, 450)
    pyautogui.click()
    pass_word_list = ['a', 'b', 'c', 'd', 'e',
                      'f', 'g', 'h', 'i', 'j',
                      'k', 'l', 'm', 'n', 'o',
                      'p', 'q', 'r', 's', 't',
                      'u', 'v', 'w', 'x', 'y',
                      'z', '0', '1', '2', '3',
                      '4', '5', '6', '7', '8', '9', '.']
    pyautogui.PAUSE = 0
    for i in range(15):
        pyautogui.press(random.choice(pass_word_list))
    pyautogui.PAUSE = 1
    pyautogui.moveTo(500, 530)
    pyautogui.click()


def invite_friend():
    pyautogui.moveTo(1100, 400)
    pyautogui.click()
    # pyautogui.moveTo(850, 280)#双击我的好友
    # pyautogui.doubleClick()
    pyautogui.moveTo(850, 300)
    tt.sleep(1)
    pyautogui.click(button='right')
    pyautogui.moveTo(870, 400)
    pyautogui.click()
    pyautogui.moveTo(950, 1000)
    pyautogui.click()
    pyautogui.moveTo(500, 800)
    pyautogui.click()
    time.sleep(3)
    pyautogui.moveTo(50, 330)
    pyautogui.click()


def choice_map():
    pyautogui.moveTo(100, 200)
    pyautogui.click()
    pyautogui.moveTo(330, 270)
    pyautogui.click()
    pyautogui.moveTo(700, 400)
    pyautogui.click()
    pyautogui.moveTo(450, 620)
    pyautogui.click()


def play_game():
    pyautogui.moveTo(50, 80)
    pyautogui.click()
    tt.sleep(30)
    control_w = Thread(target=game_w)
    control_r = Thread(target=game_r)
    control_w.start()
    control_r.start()


def game_w():
    i = 0
    while True:
        ke.key_press(0x11)
        ke.key_press(left_right[i])
        i += 1
        i %= 2


def game_r():
    while True:
        ke.key_press(0x13)
        tt.sleep(5)


def stop():
    while True:
        with keyboard.Listener(on_press=on_press) as listener:  # 键盘监听
            listener.join()


def on_press(key):
    if key == keyboard.Key.f12:
        os._exit(1)  # 如果按下f12直接终止脚本


if __name__ == '__main__':
    stop = Thread(target=stop)  # 设立子线程监听键盘事件响应用户随时ESC键终止脚本
    stop.start()
    # go_house()
    # invite_friend()
    # choice_map()
    play_game()
