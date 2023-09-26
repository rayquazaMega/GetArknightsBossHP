import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, PhotoImage, Button, StringVar

from PIL import Image,ImageTk
from templatematch import GetBossHP
import os

deviceName = '127.0.0.1:7555' #网易MuMu模拟器
adbDevices = os.popen("adb devices").read()
if deviceName not in adbDevices:
    print('Trying to connent to %s' % deviceName)
    os.popen('adb connect %s' % deviceName).read()

def screenshot(filename="resolution_test.png"):
    os.popen('adb -s %s shell screencap -p /sdcard/01.png' % deviceName).read()
    os.popen('adb -s %s pull /sdcard/01.png %s' % (deviceName,filename)).read()
def update_display():
    screenshot("for_Boss_HP.png")
    image = cv2.imread("for_Boss_HP.png")
    hp_percentage,img = GetBossHP(image)

    if hp_percentage is not None:
        result_label.config(text=f"Boss HP: {hp_percentage * 100:.2f}%")
        #img = cv2.imread('marked_image.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width = img.shape[:2]
        img = cv2.resize(img, (width//2, height//2))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        image_label.config(image=img)
        image_label.image = img
    else:
        result_label.config(text="Boss HP not found")
        image_label.config(image=None)

    if auto_update:
        root.after(50, update_display)

def toggle_update_mode():
    global auto_update
    auto_update = not auto_update
    if auto_update:
        auto_update_label.set("Auto Update: On")
        update_display()
        #root.after(1000, toggle_update_mode)  # 1秒后再次触发自动更新
    else:
        auto_update_label.set("Auto Update: Off")

root = tk.Tk()
root.title("Arknights Boss HP Tracker")

auto_update = False

result_label = Label(root, text="", font=("Helvetica", 18))
result_label.pack()

image_label = Label(root)
image_label.pack()

update_button = Button(root, text="Update", command=update_display)
update_button.pack()

auto_update_label = StringVar()
auto_update_label.set("Auto Update: Off")
auto_update_button = Button(root, textvariable=auto_update_label, command=toggle_update_mode)
auto_update_button.pack()

root.lift()
root.attributes("-topmost", True)
root.mainloop()
