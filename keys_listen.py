import keyboard
from time import sleep as wait

recoil_switch = True


def recoil_off():
    global recoil_switch
    recoil_switch = False
    wait(0.3)
    return recoil_switch 


def recoil_on():
    global recoil_switch
    recoil_switch = True
    wait(0.3)
    return recoil_switch 


keyboard.add_hotkey('g', recoil_off)
keyboard.add_hotkey('w + g', recoil_off)
keyboard.add_hotkey('s + g', recoil_off)
keyboard.add_hotkey('a + g', recoil_off)
keyboard.add_hotkey('d + g', recoil_off)
keyboard.add_hotkey('w + a + g', recoil_off)
keyboard.add_hotkey('w + d + g', recoil_off)
keyboard.add_hotkey('s + a + g', recoil_off)
keyboard.add_hotkey('s + d + g', recoil_off)

keyboard.add_hotkey('1', recoil_on)
keyboard.add_hotkey('w + 1', recoil_on)
keyboard.add_hotkey('s + 1', recoil_on)
keyboard.add_hotkey('a + 1', recoil_on)
keyboard.add_hotkey('d + 1', recoil_on)
keyboard.add_hotkey('w + a + 1', recoil_on)
keyboard.add_hotkey('w + d + 1', recoil_on)
keyboard.add_hotkey('s + a + 1', recoil_on)
keyboard.add_hotkey('s + d + 1', recoil_on)

keyboard.add_hotkey('2', recoil_on)
keyboard.add_hotkey('w + 2', recoil_on)
keyboard.add_hotkey('s + 2', recoil_on)
keyboard.add_hotkey('a + 2', recoil_on)
keyboard.add_hotkey('d + 2', recoil_on)
keyboard.add_hotkey('w + a + 2', recoil_on)
keyboard.add_hotkey('w + d + 2', recoil_on)
keyboard.add_hotkey('s + a + 2', recoil_on)
keyboard.add_hotkey('s + d + 2', recoil_on)
























