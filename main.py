"""
Ticket Submit
Zachary Rosch
28APR24
Version 7.4
"""
import tkinter as tk
from tkinter import ttk
import functions
from functools import partial


# functions
def show_times_change(showtimes, title):
    current_day = ''
    current_time = ''
    # update movie poster
    global movie_poster_image
    movie_poster_image = tk.PhotoImage(file=f'./movie_posters/{title}.png')
    movie_poster['image'] = movie_poster_image
    # clear current listings
    showtimes_listbox.delete(0, tk.END)
    day_append = ""
    for i in showtimes:
        if i[0].isalpha():
            current_day = i
            continue  # because the day has changed we need to skip to the next line to get the proper time
        elif i[0].isdigit():
            current_time = i
        else:
            continue
        showtimes_listbox.insert(tk.END, current_day + " - " + current_time)


def add_to_cart(item):  # add concession items to the kart
    stripped = item.strip()
    cart_item_list.append((CartItem(stripped.split(','))))


cart_item_list = []
class CartItem:

    def __init__(self, item_name):
        self.frame_id = tk.Frame(cart)
        self.frame_id.pack()
        self.label_id = tk.Label(self.frame_id, text=item_name[0])
        self.label_id.grid(column=0, row=0, ipadx=2)
        self.price_id = tk.Label(self.frame_id, text=item_name[1])
        self.price_id.grid(column=1, row=0, ipadx=2)
        self.delete_id = tk.Button(self.frame_id, text='Remove', command=self.remove_item)
        self.delete_id.grid(column=2, row=0, ipadx=2)

        self.price = float(item_name[1])
        CartItem.update_total(self.price)

    def __del__(self):
        print('I am destroyed')

    def remove_item(self):
        self.label_id.destroy()
        self.delete_id.destroy()
        self.price_id.destroy()
        self.frame_id.destroy()
        CartItem.update_total(self.price * -1)
        self.destroy()

    def destroy(self):
        # Perform any additional cleanup or actions before destroying the object
        print('Destroying object...')
        # You might want to remove the object from any lists or collections
        cart_item_list.remove(self)

    @staticmethod
    def update_total(amount):
        total = amount

        for i in cart_item_list:
            total += i.price

        cart_price['text'] = "$" + "%.2f" % total


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
movie_names_frame = ttk.LabelFrame(showings)  # create a label to display the movie poster
movie_names_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
movie_poster_image = tk.PhotoImage(file='./movie_posters/theater_logo.png')
movie_poster = tk.Label(
    movie_names_frame,
    image=movie_poster_image
)
movie_poster.pack(side=tk.BOTTOM)
movie_times_frame = ttk.LabelFrame(showings)
movie_times_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

current_showtime = tk.IntVar()  # Listbox that shows movie times
# create the showtimes list box
showtimes_listbox = tk.Listbox(
    movie_times_frame,
    listvariable=current_showtime,
    height=10,
    selectmode=tk.SINGLE
)
showtimes_listbox.pack(expand=True, fill=tk.BOTH)

current_movie = tk.IntVar()  # radio buttons that show movie names
loop_index = 0
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
        font=('Times New Roman', 15, 'bold'),
        variable=current_movie,
        value=loop_index,
        indicatoron=False,
        command=partial(show_times_change, movie_showings, movie_name),
    )
    movies.pack(expand=True, fill=tk.BOTH)
    loop_index += 1

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
    raw = line_read.split(','[0])
    price = raw[1]
    price = '$' + price.strip()
    name = raw[0]
    name = name.strip()
    print(price)
    conces_button = tk.Button(
        concessions,
        text=name + "  -  " + price,
        font=('Times New Roman', 15, 'bold'),
        command=partial(add_to_cart, line_read),
    )
    conces_button.pack(fill=tk.X)
concessions_listing.close()

# create a cart window
cart = tk.Tk()
cart.title('Ticket Submit > Cart')
cart.geometry('250x600')
cart_frame = ttk.LabelFrame(cart)
cart_frame.pack(side=tk.TOP)
cart_total = ttk.LabelFrame(cart)
cart_total.pack(side=tk.BOTTOM)
cart_price = tk.Label(
    cart_total,
    text='total',
    font=('Times New Roman', 15, 'bold')
)
cart_price.pack(side=tk.BOTTOM, fil=tk.X)

showings.mainloop()
concessions.mainloop()
cart.mainloop()
