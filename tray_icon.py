# Libraries
import sounddevice as sd
from tkinter.ttk import *
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
import pystray
from pystray import Icon as icon, Menu as menu, MenuItem as item


GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

main_frame = None

class Tray_Icon:
    global main_frame

    def create_tray_icon():
        tray_icon_image = Image.open('./Resources/Images/mic.png')

        menu = pystray.Menu(pystray.MenuItem('Quit', Tray_Icon.quit_window), pystray.MenuItem('Show', Tray_Icon.show_window, default=True))
        icon = pystray.Icon("Quit", tray_icon_image, "Show", menu)
        icon.run()

    def quit_window(icon, item):
        icon.stop()
        main_frame.destroy()

    def show_window(icon, item):
        icon.stop()
        main_frame.after(0,main_frame.deiconify)

class Main_Form(tk.Tk):
    def __init__(self):
        global main_frame

        super().__init__()

        self.title("app")
        self.geometry("400x550")
        self.resizable(0, 0)

        main_frame = self

        Tray_Icon.create_tray_icon()


class Event:
    @staticmethod
    def button_clicked():
        Tray_Icon.create_tray_icon()
        print("hello world")

    @staticmethod
    def main_form_closing():
        if messagebox.askokcancel("Notice", "Are you sure to close the window?"):
            main_form.destroy()


if __name__ == '__main__':
    main_form = Main_Form()
    main_form.protocol("WM_DELETE_WINDOW", Event.main_form_closing)

    main_form.mainloop()  # execute GUI
