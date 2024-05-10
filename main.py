"""
Ticket Submit
Zachary Rosch
28APR24 - 10MAY24
Version 1.0

Program allows users to order movie tickets and concession items. Once selected
    items are in the cart they can check out with a credit card.
    Once done an order file will be made in the "orders" folder.

ticket_price - price for each ticket sold.
selected_show_time - stores the selected showtime
line_read - used to store reads from files during import of data
movie_showings - stores a list of widgets that represent movies
loop_index - used to count loop iterations
"""
import tkinter as tk
from tkinter import ttk
import functions
from functools import partial
from tkinter.messagebox import showerror, showwarning, showinfo
from datetime import date
import uuid
import random

# define globals
ticket_price = 3.99
selected_show_time = None
line_read = ""
movie_showings = []
loop_index = 0

'''
 ==================   functions   ==================
'''
# when the user changes the selected move. Update the showtimes to the new movie.
# If a movie is already in the cart we need to remove it so the showtimes line up.
def show_times_change(showtimes, title):
    # if a movie is in the cart remove it.
    CartItem.delete_tickets()

    #prime local variables
    current_day = ''
    current_time = ''
    day_append = ""

    # update movie poster
    global movie_poster_image
    movie_poster_image = tk.PhotoImage(file=f'./movie_posters/{title}.png')
    movie_poster['image'] = movie_poster_image

    # clear current showtimes
    showtimes_listbox.delete(0, tk.END)

    # iterate through all the data items for the current movie.
    for i in showtimes:
        if i[0].isalpha():  # if the current data item is a day store it
            current_day = i
            continue  # because the day has changed we need to skip to the next line to get the proper time
        elif i[0].isdigit():  # if the current data item is a time store it.
            current_time = i
        else:  # if the data item is anything else, skip it.
            continue
            # update the list box item with the new time
        showtimes_listbox.insert(tk.END, current_day + " - " + current_time)

    # select the first showtime and set it into focus, so we can store it.
    showtimes_listbox.select_set(0)
    showtimes_listbox.focus_set()
    showtimes_listbox.event_generate("<<ListboxSelect>>")


# the showtime listbox can lose its selection if focus is lost.
#    store the showtime if done by the user.
def on_select(event):
    # test to make sure the listbox is in focus. if not exit the function
    focused_widget = main_window.focus_get()

    if focused_widget != showtimes_listbox:
        return

    #if in focus then store the result.
    global selected_show_time
    selected_show_time = showtimes_listbox.get(showtimes_listbox.curselection())



# add items to the kart
def add_to_cart(item, is_tickets=False):
    # because ticket items are stored in the cart we need to remember
    #   what item it is, so we can track tickets later.

    stripped = item.strip()

    # append the cart list with the new item
    cart_item_list.append((CartItem(stripped.split(','), is_tickets)))


# prepare a string to represent the movie being added. then add it to the cart.
def add_tickets_to_cart():
    # unlike concessions, tickets need a quantity with them. store that as part of the input
    quantity = float(ticket_quantity.get())
    add_to_cart(f'{current_movie.get()} X({ticket_quantity.get()}), {"%.2f" % (quantity * ticket_price)}', True)


'''
if the purchase is validated. create sale.
'''
def create_sale():
    # get information related to the sale and store it in local variables.
    buyer_name = checkout_name.get("1.0", "end-1c")
    sale_number = uuid.uuid1()

    # sale code is a short number to give to the buyer to redeem their purchase.
    #   a random number is not a good way to do this but I ran out of time :(
    #   so for now it will need to do.
    sale_code = random.randint(10000, 99999)
    movie_name = CartItem.find_movie_name()
    sale_total = cart_price['text']
    # because the showtime is a global variable bring it in scope
    global selected_show_time

    # Credit card data is only checked for format.
    #    no information is processed and card is otherwise assumed legit
    #    for the sake of the project.
    bank_transaction_number = uuid.uuid1()  # create a bank transaction number.

    # create a new text file to store the sale.
    sale_file = open(f'./orders/{buyer_name} --- {str(sale_code)}.txt', 'w')

    # write buyer name, bank transaction number, and move data to the file
    sale_file.write(f'Buyer_name //  {buyer_name} \n')
    sale_file.write(f'sale_code //  {sale_code} \n')
    sale_file.write(f'Bank transaction number // {bank_transaction_number}\n')
    sale_file.write(f'movie name // {movie_name} \n')
    sale_file.write(f'Show time // {selected_show_time}\n \n')

    # loop through all items in cart and add them
    sale_file.write(f'Purchased concessions --> \n')
    for i in cart_item_list:
        if i.is_ticket_item:  # skip movie ticket items
            continue
        current_conc = i.label_id['text']  # store current cart item
        sale_file.write(f' - {current_conc} \n')  # write cart item to file
    sale_file.write(f'<-- Purchased concessions \n \n')
    sale_file.write(f'Order total {sale_total} \n')  # write the sale total

    sale_file.close()
    # display a message that the sale finished and give them their code.
    showinfo(
        title='Information',
        message=f'Checkout complete! Your code is {sale_code}. \n Show it to a staff member to get your order!')


# validate purchase
def _validate_purchase():
    # retrieve relevant data from widgets
    card_number = checkout_card_num.get("1.0", "end-1c")
    card_number = card_number.strip()
    name = checkout_name.get("1.0", "end-1c")
    cvv = checkout_cv.get("1.0", "end-1c")
    cvv = cvv.strip()
    year = checkout_exp_year.get("1.0", "end-1c")
    year = year.strip()

    # check a ticket item is in the cart.
    if not CartItem.test_for_tickets():
        showerror(
            title='Error',
            message='No movie tickets in cart!')
        return

    # make sure the entry is the correct length. including dashes
    if len(card_number) != 19:
        showerror(
            title='Error',
            message='Incorrect card number length')
        return

    # ****-****-****-****
    # check the format. should be 4 4 number segments separated by dashes
    if card_number[4] != "-" or card_number[9] != "-" or card_number[14] != "-":
        showerror(
            title='Error',
            message='Incorrect card format. should be separated by dashes')
        return

    # check there are no letters in the card number
    for i in card_number:
        if not (i.isdigit() or i == "-"):
            showerror(
                title='Error',
                message=f'non numbers in card number. {i}')
            return

    # Laws prohibit numbers and symbols in names. check for those
    for i in name:
        if not (i.isalpha() or i == " "):
            showerror(
                title='Error',
                message='Names must only contain letters.')
            return

    # check the card name is valid. A valid name is first and last, or first, middle initial, and last.
    name = name.split()
    if len(name) != 2 and not (len(name) == 3 and len(name[1]) == 1):
        showerror(
            title='Error',
            message='Name field should include first and last name. And a middle initial if provided')
        return

    # check the cvv number
    if not (cvv.isdigit()) or not (len(cvv) == 3 or len(cvv) == 4):
        showerror(
            title='Error',
            message='CVV should be consist of 3 to 4 digits.')
        return

    # test the year format.
    if not (year.isdigit()) or len(year) != 4:
        showerror(
            title='Error',
            message='Invalid year.')
        return

    # if a card should have expired fail the checkout.
    today = date.today()
    month_str = checkout_exp_month.get()
    year = int(year)
    # store month names with their number. allowing us to convert
    #   from a string to a int representation
    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                  "Nov": 11, "Dec": 12}
    month_num = month_dict.get(month_str)
    card_date = date(year, month_num, 5)
    if today > card_date:
        showerror(
            title='Error',
            message='This card expired.')
        return

    # if there are no errors with card values. place order
    create_sale()


'''
================== cart items ==================
'''
# list that keeps track of all items added to the cart
cart_item_list = []


# create a class to represent cart items.
class CartItem:

    def __init__(self, item_name, is_tickets=False):
        # item_name is a string to be converted to a list.
        # is_tickets tracks if the new item is movie tickets.
        # because tickets have special cases we need to be able to track them

        # if the item is tickets and ticket items are already in the cart remove them
        if is_tickets:
            CartItem.delete_tickets()

        # create a frame for this cart item.
        self.frame_id = tk.Frame(cart_frame)
        self.frame_id.pack(side=tk.TOP)

        # create a label for the name of the item.
        self.label_id = tk.Label(self.frame_id, text=item_name[0])
        self.label_id.grid(column=0, row=0, ipadx=2)

        # create a label for the price of the item
        self.price_id = tk.Label(self.frame_id, text=item_name[1])
        self.price_id.grid(column=1, row=0, ipadx=2)

        # create a delete button for the item
        self.delete_id = tk.Button(self.frame_id, text='Remove', command=self.remove_item)
        self.delete_id.grid(column=2, row=0, ipadx=2)

        # store the price of this item
        self.price = float(item_name[1])

        # if this item is a ticket set the boolean to true.
        self.is_ticket_item = is_tickets

        # update the order total with the new cart value
        #   because the total is updated before the object is added
        #   to the list we need to prime the total with the items value
        CartItem.update_total(self.price)

    # if the item is removed from the cart destroy its widgets
    #    and remove itself from the cart list.
    def remove_item(self):
        self.label_id.destroy()
        self.delete_id.destroy()
        self.price_id.destroy()
        self.frame_id.destroy()
        # because the price is updated before the item is actually
        #   destroyed it will still be counted in the total.
        #   to fix this we prime the total with a negative number
        #   to cancel the items price
        CartItem.update_total(self.price * -1)
        self.destroy()

    # destroy the class instance.
    def destroy(self):
        cart_item_list.remove(self)

    # update the carts total value
    @staticmethod
    def update_total(amount):
        total = amount

        for i in cart_item_list:
            total += i.price

        cart_price['text'] = "$" + "%.2f" % total

    # find and remove ticket items
    @staticmethod
    def delete_tickets():
        for i in cart_item_list:
            if i.is_ticket_item:
                i.remove_item()

    # Check that there is a ticket item. used in checkout validation.
    @staticmethod
    def test_for_tickets():
        for i in cart_item_list:
            if i.is_ticket_item:
                return True
        return False

    # find the name of the movie item. used when changing movies
    @staticmethod
    def find_movie_name():
        for i in cart_item_list:
            if i.is_ticket_item:
                return i.label_id['text']


'''
 ==========================================
 =========== create main window ===========
 ==========================================
'''
# create main window
main_window = tk.Tk()
main_window.title('Ticket Submit')
main_window.geometry('600x900')

# exit the program if the main window is closed
def on_main_close():
    main_window.destroy()
    cart.destroy()

main_window.protocol("WM_DELETE_WINDOW", on_main_close)

# create a banner image
banner_image = tk.PhotoImage(file='./Ticket_submit_banner.png')
banner = tk.Label(main_window, image=banner_image)
banner.pack(side=tk.TOP)

# create a checkout button
checkout = tk.Button(
    main_window,
    text='checkout',
    command=lambda: cart.deiconify()  # unhidden the cart window.
)
checkout.pack(side=tk.TOP, anchor='nw')

# create the tabs for movie listings and concessions
tabs = ttk.Notebook(main_window)
tabs.pack(pady=10, expand=True, fill=tk.BOTH)

# create the frames to hold the windows
movies_frame = tk.Frame(tabs, width=600, height=600)
movies_frame.pack(fill='both', expand=True)
concessions_frame = tk.Frame(tabs, width=600, height=600)
concessions_frame.pack(fill='both', expand=True)

# create the frames to separate movie names from movie times
movie_names_frame = ttk.LabelFrame(movies_frame)  # create a label to display the movie poster
movie_names_frame.pack(expand=True, fill=tk.Y, side=tk.LEFT)
movie_times_frame = ttk.LabelFrame(movies_frame)
movie_times_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

# create a label to display a poster for the selected movie
movie_poster_image = tk.PhotoImage(file='./movie_posters/theater_logo.png')
movie_poster = tk.Label(
    movie_times_frame,
    image=movie_poster_image
)
movie_poster.pack(side=tk.TOP)

# create a frame to hold the ticket count spinbox and the add tickets to cart button.
ticket_add_frame = tk.Frame(
    movie_times_frame,
)
ticket_add_frame.pack(fill=tk.X)

# create a spinbox to count how many movie tickets should be bought.
ticket_quantity_var = tk.StringVar()
ticket_quantity = ttk.Spinbox(
    ticket_add_frame,
    from_=1,
    to=12,
    textvariable=ticket_quantity_var
)
ticket_quantity.pack(side=tk.LEFT, fill=tk.X)
ticket_quantity.set(1)

# create a button to add the selected movies to the cart
ticket_add_to_cart = tk.Button(
    ticket_add_frame,
    text='add to cart.',
    command=add_tickets_to_cart
)
ticket_add_to_cart.pack(side=tk.RIGHT)

# create the showtimes list box
current_showtime = tk.IntVar()  # variable to hold the current showtime selected
showtimes_listbox = tk.Listbox(
    movie_times_frame,
    listvariable=current_showtime,
    height=10,
    selectmode=tk.SINGLE
)
showtimes_listbox.pack(expand=True, fill=tk.BOTH)
showtimes_listbox.bind("<<ListboxSelect>>", on_select)
'''
 =============================================================
 ======== Load movie names and show times into memory ========
 =============================================================
'''
movie_listing = open('movie_listings.txt', "r") # open the file containing movie data
current_movie = tk.StringVar()  # radio buttons that show movie names
# populate the movie listings
while True:
    # load new data and strip it
    line_read = movie_listing.readline()
    line_read = line_read.strip()

    # if there are no more movies to add. break out of the loop
    if line_read == '':
        break
    # if the break is a format break. skip the entry
    if line_read == "-":
        continue

    # Add the movie the showings
    movie_name = line_read  # prepare the movie name for storage

    line_read = movie_listing.readline()  # prepare the movie showings for storage
    line_read = line_read.strip()
    movie_showings = list(line_read.split(','))

    # Add a radio button for each movie listing. storing the show times in its value
    movies = tk.Radiobutton(
        movie_names_frame,
        text=movie_name,
        font=('Times New Roman', 15, 'bold'),
        variable=current_movie,
        value=movie_name,
        indicatoron=False,
        command=partial(show_times_change, movie_showings, movie_name),
    )
    movies.pack(expand=True, fill=tk.BOTH, side=tk.TOP, pady=5)
    loop_index += 1

# close the file
movie_listing.close()

'''
 ==============================================================
 ================ Load concessions into memory ================
 ==============================================================
'''
# open the data file for concessions
concessions_listing = open('concessions.txt', 'r')

# add snacks to the concessions window
while True:
    # load new data and strip it
    line_read = concessions_listing.readline()
    line_read.strip()

    # if we are at the end of the list, exit the loop
    if line_read == "":
        break

    # separate the item name from its price in a list.
    raw = line_read.split(','[0])

    # store and format the price
    price = raw[1]
    price = '$' + price.strip()

    # store and format the name
    name = raw[0]
    name = name.strip()

    # create a button to represent the item.
    conces_button = tk.Button(
        concessions_frame,
        text=name + "  -  " + price,
        font=('Times New Roman', 15, 'bold'),
        # despite the split store the whole string for adding to the cart.
        command=partial(add_to_cart, line_read),
    )
    conces_button.pack(fill=tk.X)

# close the data file
concessions_listing.close()
'''
 ======================================================
 ================ create a cart window ================
 ======================================================
'''
cart = tk.Tk()
cart.title('Ticket Submit > Cart')
cart.geometry('330x600')
cart_frame = ttk.LabelFrame(cart)
cart_frame.pack(side=tk.TOP, fill=tk.BOTH)

# create a checkout frame for credit card information
checkout_frame = tk.Frame(
    cart_frame,
    relief=tk.RAISED,
    borderwidth=4
)
checkout_frame.pack(side=tk.BOTTOM, fill=tk.X)
checkout_frame.columnconfigure(0, uniform='equal')

# create text and input for the card name
checkout_text = tk.Label(checkout_frame, text='Enter first and last name')
checkout_text.grid(column=0, row=0, ipadx=3, ipady=3, columnspan=3)

checkout_name = tk.Text(checkout_frame, height=1)
checkout_name.grid(column=0, row=1, ipadx=3, ipady=3, columnspan=3)
checkout_name.insert(1.0, 'First Last')

# create text and input for the card number
checkout_text_card = tk.Label(checkout_frame, text='Enter card number.')
checkout_text_card.grid(column=0, row=2, ipadx=3, ipady=3, columnspan=3)

checkout_card_num = tk.Text(checkout_frame, height=1)
checkout_card_num.grid(column=0, row=3, ipadx=3, ipady=3, columnspan=3)
checkout_card_num.insert(1.0, '****-****-****-****')

# create a text widget to explain the expiring year and month
checkout_text_month = tk.Label(checkout_frame, text='Select exp month and year')
checkout_text_month.grid(column=0, row=4, ipadx=3, ipady=3, columnspan=2)

# create a drop-down box for each month
checkout_exp_month_var = tk.StringVar()
checkout_exp_month = ttk.Combobox(checkout_frame, textvariable=checkout_exp_month_var)
checkout_exp_month['state'] = 'readonly'
checkout_exp_month['value'] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
checkout_exp_month.grid(column=0, row=5, ipadx=3, ipady=3)
checkout_exp_month.current(0)

# create an input for the expiring year
checkout_exp_year = tk.Text(checkout_frame, height=1)
checkout_exp_year.grid(column=1, row=5, ipadx=3, ipady=3)
checkout_exp_year.insert(1.0, '2025')

# create an text label and input for the CVV number
checkout_text_month = tk.Label(checkout_frame, text='CVV')
checkout_text_month.grid(column=2, row=4, ipadx=3, ipady=3, )

checkout_cv = tk.Text(checkout_frame, height=1)
checkout_cv.grid(column=2, row=5, ipadx=3, ipady=3)
checkout_cv.insert(1.0, '536')

# create a button to submit the order
checkout_submit_btn = tk.Button(checkout_frame, text='submit order', command=_validate_purchase)
checkout_submit_btn.grid(column=0, row=6, ipadx=3, ipady=3, columnspan=3)

# arrange the columns of the checkout frame
checkout_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform='equal')


# instead of destroying the kart window intercept the x click and hide it instead
def on_close():
    cart.withdraw()

cart.protocol("WM_DELETE_WINDOW", on_close)


# create a label to show the total amount of our order
cart_total = ttk.LabelFrame(cart)
cart_total.pack(side=tk.BOTTOM)
cart_price = tk.Label(
    cart_total,
    text='total',
    font=('Times New Roman', 15, 'bold')
)
cart_price.pack(side=tk.BOTTOM, fil=tk.X)

# configure tabs
tabs.add(movies_frame, text='Listings')
tabs.add(concessions_frame, text='Concessions')
'''
 ===========================================
 ================ main loop ================
 ===========================================
'''
cart.withdraw()
main_window.mainloop()
