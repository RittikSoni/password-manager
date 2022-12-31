import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint, shuffle, choice
from turtle import title, width
import pyperclip
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    password_field.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters+password_numbers+password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    password_field.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = web_field.get()
    email = username_field.get()
    password = password_field.get()
    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title='Error', message='Fields are empty.')
    else:
        try:
            with open('data.json', 'r') as data_file:
                # reading the old data
                d = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # updating old data with new
            d.update(new_data)
            with open('data.json', 'w') as data_file:
                # saving updated data
                json.dump(d, data_file, indent=4)
        finally:
            web_field.delete(0, END)
            username_field.delete(0, END)
            password_field.delete(0, END)
        messagebox.showinfo(title='Saved', message='Saved successfully!')

#----------------------------- Search Password-------------------------#


def find_password():
    user_input = web_field.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
            for i in data:
                if i.lower() == user_input.lower():
                    messagebox.showinfo(
                        title=i, message=f'Email: {data[i]["email"]}\n Password: {data[i]["password"]}')
                    return
            messagebox.showinfo(
                title='Not found', message=f'No details for the {user_input} exists')
    except FileNotFoundError:
        messagebox.showerror(
            title='Error', message='File Not Found!, Try adding first.')


# ---------------------------- UI SETUP ------------------------------- #
#!Tk start
window = Tk()
window.title('Password manager')
logo = PhotoImage(file='logo.png')
window.iconphoto(False, logo)
window.config(padx=50, pady=50, bg='#ffffff')


#!logo/image
canvas = Canvas(height=200, width=200, bg='#ffffff', highlightthickness=0)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)


#!Labels
web_label = Label(text='Website:', bg='#ffffff').grid(row=1, column=0, pady=5)

username_label = Label(text='Email/Username:',
                       bg='#ffffff').grid(row=2, column=0, pady=5)

password_label = Label(text='Password:', bg='#ffffff').grid(
    row=3, column=0, pady=5)


#!Entry/Text fields
web_field = ttk.Entry(width=32)
web_field.grid(row=1, column=1)
web_field.focus()

username_field = ttk.Entry(width=50)
username_field.grid(row=2, column=1, columnspan=2)

password_field = ttk.Entry(width=32)
password_field.grid(row=3, column=1)


#!Buttons
generate_pass = ttk.Button(text='Generate Password', command=password_generator).grid(
    column=2, row=3)
add = ttk.Button(text='Add', width=50, command=save_data)
add.grid(column=1, row=4, columnspan=2, pady=5)
search = ttk.Button(text='Search', width=15, command=find_password)
search.grid(row=1, column=2, )

window.mainloop()
