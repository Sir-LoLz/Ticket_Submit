"""
Ticket Submit
Zachary Rosch
28APR24
Version 7.0
"""
import tkinter as tk
from tkinter import ttk
import functions
from functools import partial


# functions
def show_times_change(movie_data):
    current_day = ''
    current_time = ''
    # clear current listings
    showtimes_listbox.delete(0, tk.END)
    day_append = ""
    for i in movie_data:
        if i[0].isalpha():
            current_day = i
            continue  # because the day has changed we need to skip to the next line to get the proper time
        elif i[0].isdigit():
            current_time = i
        else:
            continue
        showtimes_listbox.insert(tk.END, current_day + " - " + current_time)



def add_to_cart(item):
    print(item + " added.")


# declare files
movie_listing = open('movie_listings.txt', "r")
concessions_listing = open('concessions.txt', 'r')

# declare variables
line_read = ""
movie_showings = []
showtimes_list = []

# create the movie listing window
showings = tk.Tk()
showings.title('Ticket Submit > showings')
showings.geometry('500x500')
# create the frames to separate movie names from movie times
movie_names_frame = ttk.LabelFrame(showings)
movie_names_frame.pack(expand=True, fill=tk.BOTH,side=tk.LEFT)
movie_poster_image = tk.PhotoImage(file='./adventure.png')
movie_poster = tk.Label(
    movie_names_frame,
    image=movie_poster_image
)
movie_poster.pack(side=tk.BOTTOM)

movie_times_frame = ttk.LabelFrame(showings)
movie_times_frame.pack(expand=True, fill=tk.BOTH,side=tk.RIGHT)


current_showtime = tk.IntVar()  # radio buttons that show movie times
# create the showtimes list box
showtimes_listbox = tk.Listbox(
    movie_times_frame,
    listvariable=current_showtime,
    height=10,
    selectmode=tk.SINGLE
)
showtimes_listbox.pack(expand=True, fill=tk.BOTH)

current_movie = tk.IntVar()  # radio buttons that show movie names
# populate the movie listings
while True:
    line_read = movie_listing.readline()
    line_read = line_read.strip()
    # if there are no more movies to add. break out of the loop
    if line_read == '':
        break
    # if the break is a format break. skip the entry
    if line_read == "-":
        continue
    # Add the movie the showings
    movie_name = line_read  # store the movie name
    line_read = movie_listing.readline()  # get the movie showings
    line_read = line_read.strip()
    movie_showings = list(line_read.split(','))
    # Add a radio button for each movie listing. storing the show times in its value
    movies = tk.Radiobutton(
        movie_names_frame,
        text=movie_name,
        variable=current_movie,
        value=movie_showings,
        indicatoron=False,
        command=partial(show_times_change, movie_showings),
    )
    movies.pack()

# create a concessions window
concessions = tk.Tk()
concessions.title('Ticket Submit > concessions')
concessions.geometry('500x500')

# add snacks to the concessions window
while True:
    line_read = concessions_listing.readline()
    line_read.strip()
    # if we are at the end of the list, exit the loop
    if line_read == "":
        break
    conces_button = tk.Button(
        concessions,
        text=line_read,
        command=partial(add_to_cart, line_read)
    )
    conces_button.pack()

# create a cart window
cart = tk.Tk()
cart.title('Ticket Submit > Cart')
cart.geometry('200x600')

showings.mainloop()
concessions.mainloop()
cart.mainloop()
