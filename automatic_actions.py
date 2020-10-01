import webbrowser
import requests
import time
import os
from pynput.keyboard import Key, Controller


#Keystrokes encapsulation. Must be in "Stack" (First in last out)
def press_and_release_control_plus_character(character):
    Keyboard=Controller()
    Keyboard.press(Key.ctrl)
    Keyboard.press(character)
    Keyboard.release(character)
    Keyboard.release(Key.ctrl)

def press_and_release_single_key(key):
    Keyboard=Controller()
    Keyboard.press(key)
    Keyboard.release(key)

def press_and_release_control_plus_shift_plus_s():
    Keyboard=Controller()
    Keyboard.press(Key.ctrl)
    Keyboard.press(Key.shift)
    Keyboard.press('s')
    Keyboard.release('s')
    Keyboard.release(Key.shift)
    Keyboard.release(Key.ctrl)

def type(str):
    keyboard=Controller()
    keyboard.type(str)



def action_1_open_google_docs():
    #os.system("sudo -u andreurocagrange google-chrome https://docs.new")
    webbrowser.get('google-chrome').open('https://docs.new')
    return 0

def action_2_toggle_speach_writing():
    press_and_release_control_plus_shift_plus_s()
    return 0

def action_3_selec_copy_paste_to_new_email(email_address='weteroca@gmail.com',subject='automatic_email'):
    press_and_release_control_plus_character('a')
    press_and_release_control_plus_character('c')
    webbrowser.get('google-chrome').open('https://mail.google.com/mail/u/0/#inbox?compose=new')
    time.sleep(10)
    type(email_address)
    time.sleep(0.1)
    press_and_release_single_key(Key.tab)
    time.sleep(0.1)
    type(subject)
    time.sleep(0.1)
    press_and_release_single_key(Key.tab)
    press_and_release_control_plus_character('v')
    press_and_release_control_plus_character(Key.enter)





if __name__ == '__main__':
    #full iteration working.
    action_1_open_google_docs()
    time.sleep(5)
    action_2_toggle_speach_writing()
    time.sleep(10)
    action_2_toggle_speach_writing()
    time.sleep(1)
    action_3_selec_copy_paste_to_new_email()
#    action_2_toggle_speach_writing()
