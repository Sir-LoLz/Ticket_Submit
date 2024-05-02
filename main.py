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
def change_show_times(movie_data):
    # print(current_movie)
    print(movie_data)



def add_to_cart(item):
    print(item + " added.")


# declare files
movie_listing = open('movie_listings.txt', "r")
concessions_listing = open('concessions.txt', 'r')

# create the movie listing window
showings = tk.Tk()
showings.title('Ticket Submit > showings')
showings.geometry('500x500')
# create the frames to separate movie names from movie times


# declare variables
line_read = ""
movie_showings = []
current_movie = tk.IntVar()  # radio buttons that show movie names
current_showtimes = tk.IntVar()  # radio buttons that show movie times

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
        showings,
        text=movie_name,
        variable=current_movie,
        value=movie_showings,
        indicatoron=False,
        #command=change_show_times)
        command=partial(change_show_times, movie_showings),
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
        command=partial(add_to_cart,line_read)
    )
    conces_button.pack()


# create a cart window
cart = tk.Tk()
cart.title('Ticket Submit > Cart')
cart.geometry('200x600')


showings.mainloop()
concessions.mainloop()
cart.mainloo()