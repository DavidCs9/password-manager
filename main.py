from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(6, 6)
    nr_symbols = randint(2, 2)
    nr_numbers = randint(2, 2)

    password_letters = [choice(letters) for char in range(nr_letters)]
    password_symbols = [choice(symbols) for char in range(nr_symbols)]
    password_numbers = [choice(numbers) for char in range(nr_numbers)]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    website = website_entry.get()
    email = email_entry.get()
    new_pass = pass_entry.get()
    new_data = {
        website: {
            'email': email,
            'password': new_pass
        }
    }
    if website != '' and email != '' and new_pass != '':
        # if info is correct
        is_ok = messagebox.askquestion(title=website, message=f'These are the details entered: \nEmail: {email}'
                                                              f'\nPassword: {new_pass}'
                                                              f'\nIts the info correct?')
        if is_ok == 'yes':
            try:
                with open('data.json', 'r') as data_file:
                    # reading old data
                    data = json.load(data_file)
                    # updating old data with new data
                    data.update(new_data)
            except FileNotFoundError:
                with open('data.json', 'w') as db:
                    # creating a data file if not exist
                    json.dump(new_data, db, indent=4)
            else:
                with open('data.json', 'w') as db:
                    # saving updated data
                    json.dump(data, db, indent=4)
            finally:
                website_entry.delete(0, END)
                pass_entry.delete(0, END)

    else:
        messagebox.showerror('Missing Argument', 'You leaving fields empty')


# ---------------------------- SEARCH ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            # reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f'No Data File Found')
    if website in data:
        messagebox.showinfo(title='Website', message=f'{website}\n'
                                                     f'Email: {data[website]["email"]}\n'
                                                     f'Password: {data[website]["password"]}'
                            )
    else:
        messagebox.showinfo(title="Error", message=f'{website} is not registered')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(pady=60, padx=60)
logo = PhotoImage(file='logo.png')

canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# website
website_label = Label(text='Website:')
website_label.grid(row=1, column=0)
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()
search_button = Button(text="             Search           ", command=search)
search_button.grid(row=1, column=2)

# email
email_label = Label(text='Email/Username:')
email_label.grid(row=2, column=0)
email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, 'davidcastrosihotmail.com')

# pass
pass_label = Label(text='Password:')
pass_label.grid(row=3, column=0)
pass_entry = Entry(width=33, show='*')
pass_entry.grid(row=3, column=1)

generate_pass_btn = Button(text='Generate Password', command=generate_pass)
generate_pass_btn.grid(row=3, column=2)

# add
add_btn = Button(
    text='                                            Add                                                  ',
    command=save_pass)
add_btn.grid(row=4, column=1, columnspan=2)

window.mainloop()
