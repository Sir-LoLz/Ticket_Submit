import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

radio_list = []


class RadioButtons(ttk.Radiobutton):
    buttons_list = []
    selected_movie = ""

    def __init__(self):
        ttk.Radiobutton.__init__(
            self,
            root,
            text='hello',
            value=len(RadioButtons.buttons_list) + 1
        )

        RadioButtons.buttons_list.append(self)
        self.pack()

    @classmethod
    def destroy_buttons(cls):
        for i in RadioButtons.buttons_list:
            i.destroy()

        RadioButtons.buttons_list = []
        global radio_list
        radio_list = []
        print("destroyed")


root = tk.Tk()
root.title("Tkinter Window")
root.geometry("300x300")

check_button = tk.Button(
    text='check list',
    command=lambda: print(RadioButtons.buttons_list),
)
check_button.pack()

check_button2 = tk.Button(
    text='check list',
    command=lambda: print(radio_list),
)
check_button2.pack()

make_button = tk.Button(
    text='make radio button',
    command=lambda: radio_list.append(RadioButtons())
)
make_button.pack()

kill_buttons = tk.Button(
    text='destroy radio button',
    command=lambda: RadioButtons.destroy_buttons()
)
kill_buttons.pack()

wind_buttons = tk.Button(
    text='show all buttons',
    command=lambda: print(root.winfo_children())
)
wind_buttons.pack()

root.mainloop()