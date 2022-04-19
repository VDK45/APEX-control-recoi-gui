# -*- coding: utf-8 -*-

import os
import json
import sys
import threading
import time
import win32api
import win32con
import winsound
import ctypes
from image_search import get_screen_area_as_image, load_image_from_file, search_image_in_image
from overlay_label import OverlayLabel
from keyboard_input import keyb_down, keyb_up
import pathlib
from pathlib import Path
import keys_listen as key
import gui



LMB = win32con.VK_LBUTTON
F4 = win32con.VK_F4
F10 = win32con.VK_F10
NUM_4 = win32con.VK_NUMPAD4
NUM_6 = win32con.VK_NUMPAD6
KEY_1 = 0x31
KEY_2 = 0x32
KEY_3 = 0x33
KEY_E = 0x45
KEY_R = 0x52
SHOP = True


EMPTY_WEAPONS_LIST = [
    {
        "name": "None",
        "rpm": 6000,
        "check_image": None,
        "check_area": [1352, 701, 1382, 731],
        "pattern": [
            [0,0],
        ]
    },
]

# for cursor detector
class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int),
                ('y', ctypes.c_int)]

class CURSORINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint),
                ('flags', ctypes.c_uint),
                ('hCursor', ctypes.c_void_p),
                ('ptScreenPos', POINT)]
               


def beep_on():
    winsound.Beep(2000, 100)


def beep_off():
    winsound.Beep(1000, 100)


def beep_exit():
    winsound.Beep(500, 500)


def mouse_move_relative(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)


def lmb_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def lmb_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def rmb_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)


def rmb_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def is_lmb_pressed():
    return win32api.GetKeyState(LMB) < 0


def cursor_detector():
    # Load and set argument types
    GetCursorInfo = ctypes.windll.user32.GetCursorInfo
    GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
    # Initialize the output structure
    info = CURSORINFO()
    info.cbSize = ctypes.sizeof(info)
    # Do it!
    if GetCursorInfo(ctypes.byref(info)):
        if info.flags & 0x00000001:
            return True
        else:
            return False
    else:
        print("WARNING: Cursor detector is not running!")


def load_weapons():
    weapons_list = EMPTY_WEAPONS_LIST
    current_weapon_index = 0
    weapon_filepath = "./weapon_data/apex.json"
    #print("DEBUG: Opening and load data from {}".format(weapon_filepath))
    try:
        with open(weapon_filepath) as f:
            data = json.load(f)
            weapons_data = data["weapons"]
    except:
        print("ERROR: Can not open/read file with weapon data!")
        print("INFO: ERROR! Use default EMPTY_WEAPONS_LIST. Check data files!")
        return weapons_list, current_weapon_index
    #print("DEBUG: Ready!")

    weapons_list = weapons_data

    for i, weapon in enumerate(weapons_list):
        if weapon["check_image"]:
            image = load_image_from_file("./weapon_data/apex_img\{}".format(weapon["check_image"]))
            weapons_list[i]["image"] = image
        else:
            weapons_list[i]["image"] = None

    return weapons_list, current_weapon_index


def toggle_recoil(no_recoil):
    if no_recoil == True:
        beep_off()
    else:
        beep_on()
    return not no_recoil


def prev_weapon(weapons_list, current_weapon_index):
    if current_weapon_index < 1:
        current_weapon_index = len(weapons_list) - 1
    else:
        current_weapon_index -= 1
    return current_weapon_index


def next_weapon(weapons_list, current_weapon_index):
    if current_weapon_index > len(weapons_list) - 2:
        current_weapon_index = 0
    else:
        current_weapon_index += 1
    return current_weapon_index


def get_tick(rpm):
    rps = rpm/60
    mstick = 1000.0/rps
    stick = round(mstick/1000, 3)
    return stick


def construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil):
    recoil_data = "ON" if no_recoil else "OFF/GRENADE"
    bg_data = "#acffac" if no_recoil else "#ffacac"
    recoil_string = "No recoil+: {}".format(recoil_data)
    weapon_string = "Weapon: {}".format(weapons_list[current_weapon_index]["name"])
    length = max(len(recoil_string), len(weapon_string))
    overlay_string = "{}\n{}".format(recoil_string.ljust(length), weapon_string.ljust(length))
    overlay.set_bg(bg_data)
    overlay.set_text(overlay_string)


def process_no_recoil(overlay, weapons_list, current_weapon_index, no_recoil):
    global M_SENS
    shot_index = 0
    shot_tick = get_tick(weapons_list[current_weapon_index]["rpm"])
    while is_lmb_pressed():
        current_pattern = weapons_list[current_weapon_index]["pattern"]
        

        if shot_index < len(current_pattern) - 1:
            dx = -(current_pattern[shot_index][0] + gui.M_SENS)
            dy = -(current_pattern[shot_index][1] + gui.M_SENS)
            mouse_move_relative(dx, dy)
            time.sleep(shot_tick)
            shot_index += 1
            construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil)


def detect_current_weapon(weapons_list):
    for index, weapon in enumerate(weapons_list):
        if weapon["image"] is not None:
            found_xy = None
            try:
                image_to_check = get_screen_area_as_image(weapon["check_area"])
                found_xy = search_image_in_image(weapon["image"], image_to_check)
            except:
                print("Can not read images. Check folder weapon_data!")
            if found_xy:
                return index
    return None


class WeaponDetectorThread(threading.Thread):
    def __init__(self, weapon_list):
        threading.Thread.__init__(self)
        self.weapon_list = weapon_list
        self.out = None
        self.no_recoil = False
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            if self.no_recoil:
                weapon_autodetect = detect_current_weapon(self.weapon_list)
                self.out = weapon_autodetect
            time.sleep(0.05)

    def terminate(self):
        self.shutdown = True



def main():
    running = True
    no_recoil = False
    key.recoil_switch = True
    weapons_list, current_weapon_index = load_weapons()
    overlay = OverlayLabel()
    overlay.set_size(20, 2)  # size in symbols
    print("INFO: Starting WeaponDetector daemon...")
    weapon_detector = WeaponDetectorThread(weapons_list)
    weapon_detector.setDaemon(True)
    weapon_detector.start()
    print("INFO: Ready!")
    print("INFO: F10 - Exit program")
    print("INFO: FULL VERSION")
    no_recoil = toggle_recoil(no_recoil)
    weapon_detector.no_recoil = no_recoil
    state_left = win32api.GetKeyState(0x01)  # L mouse
    state_right = win32api.GetKeyState(0x02)  # R mouse
    
    while running:
        weapons_list, current_weapon_index = load_weapons()
        if weapon_detector.out is not None:
            current_weapon_index = weapon_detector.out
        construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil)
#        if win32api.GetAsyncKeyState(F4):
#            no_recoil = toggle_recoil(no_recoil)
#            weapon_detector.no_recoil = no_recoil
#            time.sleep(0.2)
        if win32api.GetAsyncKeyState(F10):
            running = not running
            beep_exit()
            weapon_detector.terminate()
            print("INFO: Exiting!")
            time.sleep(0.5)
        if is_lmb_pressed() and no_recoil and not cursor_detector():
            process_no_recoil(overlay, weapons_list, current_weapon_index, no_recoil)
            time.sleep(0.02)
        if win32api.GetAsyncKeyState(0x09) or win32api.GetAsyncKeyState(0x1B):
            SHOP = False
        if win32api.GetAsyncKeyState(0x45):
            SHOP = True
        if current_weapon_index == 1 and gui.SHOP == True and SHOP == True:
            if win32api.GetAsyncKeyState(0x09) or win32api.GetAsyncKeyState(0x1B):
                SHOP = False
            keyb_down(0x41)
            time.sleep(0.1)
            keyb_up(0x41)
            
            if win32api.GetAsyncKeyState(0x09) or win32api.GetAsyncKeyState(0x1B):
                SHOP = False
            time.sleep(0.02)
            if win32api.GetAsyncKeyState(0x09) or win32api.GetAsyncKeyState(0x1B):
                SHOP = False
            keyb_down(0x44)
            time.sleep(0.1)
            keyb_up(0x44)
            if win32api.GetAsyncKeyState(0x09) or win32api.GetAsyncKeyState(0x1B):
                SHOP = False
            current_weapon_index = 0
        if current_weapon_index == 2:
            keyb_down(0x70)
            time.sleep(0.2)
            keyb_up(0x70)
            current_weapon_index = 0
            time.sleep(1.5)
        if current_weapon_index == 3:
            keyb_down(0x20)
            time.sleep(0.2)
            keyb_up(0x20)
            current_weapon_index = 0
            time.sleep(0.8)
        if key.recoil_switch == True:
            no_recoil = True
            weapon_detector.no_recoil = no_recoil
        if key.recoil_switch == False:
            no_recoil = False
            weapon_detector.no_recoil = no_recoil
        mouse_1 = win32api.GetKeyState(0x01)
        if mouse_1 != state_left:  # mouse 1 release 
            state_left = mouse_1
            if mouse_1 >= 0:
                key.recoil_switch = True
                no_recoil = True
                current_weapon_index = 0
        
        
                                                


if __name__ == "__main__":
    print("https://www.patreon.com/vdk45")
    print("Внимание: Только для английской версии")
    print("Внимание: Чтобы overlay отображался играть в окне или без рамки (Не в польноэкраном режиме)")
    print("Внимание: Разрешение экрана только: 1920 × 1080")
    print("Не закрывайте это окно!")
    print("Attention: English version only")
    print("Attention: To have the overlay displayed play in a window or without a border (Not in full screen mode)")
    print("Attention: Resolution screen only: 1920×1080")
    print("Don't close this window!")
    
    
    main()
