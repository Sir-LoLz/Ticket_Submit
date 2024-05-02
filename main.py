"""
Ticket Submit
Zachary Rosch
28APR24
Version 7.1
"""
import tkinter as tk
from tkinter import ttk
import functions
from functools import partial


# classes
class Movies(ttk.Radiobutton):
    buttons_list = []
    selected_movie = ""

    def __init__(self):
        ttk.Radiobutton.__init__(
            self,
            showings,
            text='hello',
            value=len(Movies.buttons_list) + 1
        )

        Movies.buttons_list.append(self)
        self.pack()

    @classmethod
    def create_listing_data(cls):  # populate the movie listings
        movie_listing = open('movie_listings.txt', "r")
        line_read = ""
        movie_showings = ""
        current_movie = tk.StringVar()

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
                # command=change_show_times
                command=lambda: Movies.add_show_times(current_movie)
            )
            movies.pack()

        movie_listing.close()  # close the move txt file

    def add_show_times(current_movie):  # populate the showtimes
        print(current_movie.get())
        data = list(current_movie.get())
        print(data)
        #for i in data:
         #   print(i)


    @classmethod
    def remove_show_times(cls):  # remove all showtimes
        for i in Movies.buttons_list:
            i.destroy()

        Movies.buttons_list = []
        print("destroyed")


# functions
def change_show_times(movie_data):
    pass


def add_to_cart(item):
    print(item + " added.")


# create the movie listing window
showings = tk.Tk()
showings.title('Ticket Submit > showings')
showings.geometry('500x500')
# create the frames to separate movie names from movie times

Movies.create_listing_data()  # create the movie listings

if __name__ == '__main__':
    showings.mainloop()
