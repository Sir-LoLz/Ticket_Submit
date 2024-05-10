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
"""
import tkinter as tk
from tkinter import ttk
import functions
from functools import partial
from tkinter.messagebox import showerror, showwarning, showinfo
from datetime import date
import uuid

'''
set the global price of tickets.
'''
ticket_price = 3.99

selected_show_time = None


# functions
def show_times_change(showtimes, title):
    #remove current film from cart
    CartItem.delete_tickets()

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
        showtimes_listbox.select_set(0)
        showtimes_listbox.focus_set()
        showtimes_listbox.event_generate("<<ListboxSelect>>")


def on_select(event):
    #test to make sure a time is selected
    focused_widget = main_window.focus_get()
    if focused_widget != showtimes_listbox:
        print("not selected.")
        return
    global selected_show_time
    selected_show_time = showtimes_listbox.get(showtimes_listbox.curselection())
    print(selected_show_time)


def add_to_cart(item, is_tickets=False):  # add concession items to the kart
    stripped = item.strip()
    print(stripped)
    cart_item_list.append((CartItem(stripped.split(','), is_tickets)))


# prepare a string to represent the movie being added. then add it to the cart.
def add_tickets_to_cart():
    quantity = float(ticket_quantity.get())

    add_to_cart(f'{current_movie.get()} X({ticket_quantity.get()}), {"%.2f" % (quantity * ticket_price)}', True)


'''
if the purchase is validated. create sale.
'''


def get_selected_item():
    selected_index = showtimes_listbox.curselection()
    if selected_index:  # Check if anything is selected
        item = showtimes_listbox.get(selected_index[0])
        print("Selected item:", item)
        return item
    else:
        print("No item selected")


def create_sale():
    buyer_name = checkout_name.get("1.0", "end-1c")
    sale_number = uuid.uuid1()
    movie_name = CartItem.find_movie_name()
    sale_total = cart_price['text']
    global selected_show_time

    # Credit card data is only checked for format.
    #    no information is processed and card is otherwise assumed legit
    #    for the sake of the project.
    bank_transaction_number = uuid.uuid1()
    sale_file = open(f'./orders/{buyer_name}---{str(sale_number)}.txt', 'w')
    sale_file.write(f'Buyer_name //  {buyer_name} \n')
    sale_file.write(f'Bank transaction number // {bank_transaction_number}\n')
    sale_file.write(f'movie name // {movie_name} \n')
    sale_file.write(f'Show time // {selected_show_time}\n \n')
    # loop through all items in cart and add them
    sale_file.write(f'Purchased concessions --> \n')
    for i in cart_item_list:
        if i.is_ticket_item:
            continue
        current_conc = i.label_id['text']
        sale_file.write(f'{current_conc} \n')
    sale_file.write(f'<-- Purchased concessions \n \n')
    sale_file.write(f'Order total {sale_total} \n')

    sale_file.close()
    showinfo(
        title='Information',
        message='Checkout complete!')


# validate purchase
def _validate_purchase():
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

    # make sure the entry is the correct length
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
    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                  "Nov": 11, "Dec": 12}
    month_num = month_dict.get(month_str)
    print(f'month num  {month_str}')
    card_date = date(year, month_num, 5)
    if today > card_date:
        showerror(
            title='Error',
            message='This card expired.')
        return

    # if there are no errors with card values. place order
    create_sale()


# list that keeps track of all items added to the cart
cart_item_list = []


# create a class to represent cart items
class CartItem:
    ticket_item = None

    def __init__(self, item_name, is_tickets=False):

        # if the item is tickets and ticket items are already in the cart remove them
        if is_tickets:
            CartItem.delete_tickets()

        self.frame_id = tk.Frame(cart_frame)
        self.frame_id.pack(side=tk.TOP)
        self.label_id = tk.Label(self.frame_id, text=item_name[0])
        self.label_id.grid(column=0, row=0, ipadx=2)
        self.price_id = tk.Label(self.frame_id, text=item_name[1])
        self.price_id.grid(column=1, row=0, ipadx=2)
        self.delete_id = tk.Button(self.frame_id, text='Remove', command=self.remove_item)
        self.delete_id.grid(column=2, row=0, ipadx=2)
        self.price = float(item_name[1])
        self.is_ticket_item = is_tickets
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

    # find and remove ticket items
    @staticmethod
    def delete_tickets():
        for i in cart_item_list:
            if i.is_ticket_item:
                i.remove_item()

    # Check that there is a ticket item
    @staticmethod
    def test_for_tickets():
        for i in cart_item_list:
            if i.is_ticket_item:
                return True
        return False

    # find the name of the movie item
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

# create a banner image
banner_image = tk.PhotoImage(file='./Ticket_submit_banner.png')
banner = tk.Label(main_window,image=banner_image)
banner.pack(side= tk.TOP)

# create a checkout button
checkout = tk.Button(
    main_window,
    text='checkout',
    command=lambda: cart.deiconify()
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

# declare variables
line_read = ""
movie_showings = []
showtimes_list = []

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

current_showtime = tk.IntVar()  # variable to hold the current showtime selected
# create the showtimes list box
showtimes_listbox = tk.Listbox(
    movie_times_frame,
    listvariable=current_showtime,
    height=10,
    selectmode=tk.SINGLE
)

showtimes_listbox.pack(expand=True, fill=tk.BOTH)
showtimes_listbox.bind("<<ListboxSelect>>", on_select)

# =============================================================
# ======== Load movie names and show times into memory ========
# =============================================================
movie_listing = open('movie_listings.txt', "r")
current_movie = tk.StringVar()  # radio buttons that show movie names
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
        value=movie_name,
        indicatoron=False,
        command=partial(show_times_change, movie_showings, movie_name),
    )
    movies.pack(expand=True, fill=tk.BOTH, side=tk.TOP, pady=5)
    loop_index += 1

movie_listing.close()

# ==============================================================
# ================ Load concessions into memory ================
# ==============================================================
concessions_listing = open('concessions.txt', 'r')
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
        concessions_frame,
        text=name + "  -  " + price,
        font=('Times New Roman', 15, 'bold'),
        command=partial(add_to_cart, line_read),
    )
    conces_button.pack(fill=tk.X)
concessions_listing.close()

# ======================================================
# ================ create a cart window ================
# ======================================================
cart = tk.Tk()
cart.title('Ticket Submit > Cart')
cart.geometry('300x600')
cart_frame = ttk.LabelFrame(cart)
cart_frame.pack(side=tk.TOP, fill=tk.BOTH)

# create a checkout frame that takes credit card information
checkout_frame = tk.Frame(
    cart_frame,
    relief=tk.RAISED,
    borderwidth=4
)
checkout_frame.pack(side=tk.BOTTOM, fill=tk.X)
checkout_frame.columnconfigure(0, uniform='equal')

checkout_text = tk.Label(checkout_frame, text='Enter first and last name')
checkout_text.grid(column=0, row=0, ipadx=3, ipady=3, columnspan=3)

checkout_name = tk.Text(checkout_frame, height=1)
checkout_name.grid(column=0, row=1, ipadx=3, ipady=3, columnspan=3)
checkout_name.insert(1.0, 'name fdgfd')

checkout_text_card = tk.Label(checkout_frame, text='Enter card number.')
checkout_text_card.grid(column=0, row=2, ipadx=3, ipady=3, columnspan=3)

checkout_card_num = tk.Text(checkout_frame, height=1)
checkout_card_num.grid(column=0, row=3, ipadx=3, ipady=3, columnspan=3)
#checkout_card_num.insert(1.0, '****-****-****-****')
checkout_card_num.insert(1.0, '1234-1234-1234-1234')

checkout_text_month = tk.Label(checkout_frame, text='Select exp month and year')
checkout_text_month.grid(column=0, row=4, ipadx=3, ipady=3, columnspan=2)

checkout_exp_month_var = tk.StringVar()
checkout_exp_month = ttk.Combobox(checkout_frame, textvariable=checkout_exp_month_var)
checkout_exp_month['state'] = 'readonly'
checkout_exp_month['value'] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
checkout_exp_month.grid(column=0, row=5, ipadx=3, ipady=3)
checkout_exp_month.current(0)

checkout_exp_year = tk.Text(checkout_frame, height=1)
checkout_exp_year.grid(column=1, row=5, ipadx=3, ipady=3)
checkout_exp_year.insert(1.0, '2025')

checkout_text_month = tk.Label(checkout_frame, text='CVV')
checkout_text_month.grid(column=2, row=4, ipadx=3, ipady=3, )

checkout_cv = tk.Text(checkout_frame, height=1)
checkout_cv.grid(column=2, row=5, ipadx=3, ipady=3)
checkout_cv.insert(1.0, '536')

checkout_submit_btn = tk.Button(checkout_frame, text='submit order', command=_validate_purchase)
checkout_submit_btn.grid(column=0, row=6, ipadx=3, ipady=3, columnspan=3)

checkout_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform='equal')


# instead of destroying the kart window intercept the x click and hide it instead
def on_close():
    print("done")
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

# ===========================================
# ================ main loop ================
# ===========================================
cart.withdraw()
#main_window.withdraw()
main_window.mainloop()
