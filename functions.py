import tkinter as tk
from tkinter import ttk

"""
def movie_add(name,showtimes):
    print("movie name is " + name)
    for i in showtimes:
        print(i)
"""


def movie_add(name, showtimes, window):
    tk.Radiobutton(window, text=name, variable=showtimes
                   )
