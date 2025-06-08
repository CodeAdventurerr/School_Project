import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import database

#modules
import smtplib #Send Mail Transfer Protocol Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

app = customtkinter.CTk()
app.title('Hendecabytes')
app.geometry('600x600')
app.config(bg='#18161D')
app.resizable(False, False)

font1 = ('Arial', 25, 'bold')
font2 = ('Arial', 13, 'bold')
font3 = ('Arial', 18, 'bold')


def add_to_treeview():
    tickets = database.get_tickets()
    tree.delete(*tree.get_children())
    for ticket in tickets:
        if ticket[2] > 0:
            tree.insert('', END, values=ticket)


def reservation(name, movie, quantity, price):
    customer_name = name
    movie_name = movie
    booked_quantity = quantity
    ticket_price = price
    price = ticket_price * booked_quantity

    frame = customtkinter.CTkFrame(app, bg_color='#18161D', fg_color='#292929', corner_radius=10, border_width=2,
                                   border_color='#0f0', width=200, height=130)
    frame.place(x=190, y=450)

    name_label = customtkinter.CTkLabel(frame, font=font3, text=f'Name:{customer_name}', text_color='#fff',
                                        bg_color='#292933')
    name_label.place(x=10, y=10)

    movie_label = customtkinter.CTkLabel(frame, font=font3, text=f'Movie:{movie_name}', text_color='#fff',
                                         bg_color='#292933')
    movie_label.place(x=10, y=50)

    total_price_label = customtkinter.CTkLabel(frame, font=font3, text=f'Total Price:{price}', text_color='#fff',
                                               bg_color='#292933')
    total_price_label.place(x=10, y=90)

    return price


def book():
    customer_name = name_entry.get()
    customer_email = email_entry.get()  # Added customer_email variable

    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a ticket to book.')
    elif not customer_name:
        messagebox.showerror('Error', 'Enter customer name.')
    else:
        row = tree.item(selected_item)['values']
        movie_name = row[1]
        ticket_price = row[3]
        booked_quantity = int(variable1.get())
        if booked_quantity > row[2]:
            messagebox.showerror('Error', 'No enough tickets.')
        else:
            database.update_quantity(row[0], booked_quantity)
            add_to_treeview()
            price = reservation(customer_name, movie_name, booked_quantity, ticket_price)  # Pass the 'ticket_price' argument
            with open('Tickets.txt', 'a') as file:
                file.write(f'Customer Name: {customer_name}\n')
                file.write(f'Movie Name: {movie_name}\n')
                file.write(f'Total Price: {price}$\n=====================\n')
            messagebox.showinfo('Success', 'Tickets are booked!')

            # Script for transmitting a message to specified gmail account (receipt)
            def send_email(smtp_server, port, sender, password, recipients, subject, body_format_string):

                # Instantiate a variable for MIMEMultipart import
                msg = MIMEMultipart()

                body = body_format_string.format(recipients = ', '.join(recipients))

                # add the values for sender, recipients and subject of the message
                msg['From'] = sender
                msg['To'] = ','.join(recipients)
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # Declaration of variable for import smtp or Send Mail Transfer Protocol and assign values
                server = smtplib.SMTP(smtp_server, port, timeout=60)
                server.starttls()
                server.login(sender, password)
                text = msg.as_string()
                server.sendmail(email, recipients, text)
                server.send_message(msg)
                server.quit()

            # Transfer Protocol Server and Port
            smtp_server = 'smtp.gmail.com'
            port = 587

            # variable declaration for sender's gmail  account email and password
            email = 'YourEmail@gmail.com'
            password = 'Yourpassword'

            # Preparation for recipient (No Assigned Values coz the user will input that in console)
            fullname = customer_name
            recipients = customer_email

            # Expiry date of email
            expiration_Date = datetime.now() + timedelta(days=3)

            subject = 'Movie Ticket Receipt'

            # Body of the message sent
            body_format_string = f"""
             Hello!,

             This is your receipt for purchasing ticket.

             Recipient's Name: {fullname}
             Movie Name: {movie_name}
             Booked Quantity: {booked_quantity}
             Price: {price}
             Sent by: Movie Cinema Inc.
             Expiry Date: {expiration_Date.strftime("%Y-%m-%d")}

             Thank you for purchasing your ticket!,

             - HendecaBytes
             """

            send_email(smtp_server, port, email, password, recipients, subject, body_format_string)

title1_label = customtkinter.CTkLabel(app, font=font1, text='Available Film', text_color='#fff', bg_color='#18161D')
title1_label.place(x=200, y=20)

image1 = PhotoImage(file="film-reel.png")
image1_label = Label(app, image=image1, bg='#18161D')
image1_label.place(x=30, y=10)

image2 = PhotoImage(file="movie-ticket.png")
image2_label = Label(app, image=image2, bg='#18161D')
image2_label.place(x=80, y=5)

name_label = customtkinter.CTkLabel(app, font=font3, text='Customer Name:', text_color='#fff', bg_color='#18161D')
name_label.place(x=120, y=300)

name_entry = customtkinter.CTkEntry(app, font=font3, text_color='#000', fg_color='#fff', border_color='#AA04A7',
                                    border_width=2, width=160)
name_entry.place(x=290, y=300)

name_label = customtkinter.CTkLabel(app, font=font3, text='Customer Name:', text_color='#fff', bg_color='#18161D')
name_label.place(x=120, y=300)

email_label = customtkinter.CTkLabel(app, font=font3, text='Customer Email:', text_color='#fff', bg_color='#18161D')
email_label.place(x=120,y=345)

email_entry = customtkinter.CTkEntry(app, font=font3, text_color='#000', fg_color='#fff', border_color='#AA04A7', border_width=2, width=160)
email_entry.place(x=290, y=345)

number_label = customtkinter.CTkLabel(app, font=font3, text='No. of Tickets:', text_color='#fff', bg_color='#18161D')
number_label.place(x=122, y=390)

variable1 = StringVar()
options = ['1', '2', '3', '4', '5', '6']

duration_options = customtkinter.CTkComboBox(app, font=font3, text_color='#000', fg_color='#fff',
                                             dropdown_hover_color='#AA04A7', button_color='#AA04A7',
                                             button_hover_color='#AA04A7', border_color='#AA04A7', width=160,
                                             variable=variable1, values=options, state='readonly')
duration_options.set('1')
duration_options.place(x=290, y=390)

book_button = customtkinter.CTkButton(app, command=book, font=font3, text_color='#fff', text='Book Tickets',
                                      fg_color='#AA04A7', hover_color='#6D0068', bg_color='#18161D', cursor='hand2',
                                      corner_radius=15, width=200)
book_button.place(x=190, y=450)

style = ttk.Style(app)

style.theme_use('clam')
style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='292933')
style.map('Treeview', background=[('selected', '#AA04A7')])

tree = ttk.Treeview(app, height=8)

tree['columns'] = ('Ticket ID', 'Movie Name', 'Available Tickets', 'Ticket Price')

tree.column('#0', width=0, stretch=tk.NO)
tree.column('Ticket ID', anchor=tk.CENTER, width=100)
tree.column('Movie Name', anchor=tk.CENTER, width=100)
tree.column('Available Tickets', anchor=tk.CENTER, width=100)
tree.column('Ticket Price', anchor=tk.CENTER, width=100)

tree.heading('Ticket ID', text='Ticket ID')
tree.heading('Movie Name', text='Movie Name')
tree.heading('Available Tickets', text='Available Tickets')
tree.heading('Ticket Price', text='Ticket Price')

tree.place(x=90, y=95)

add_to_treeview()

app.mainloop()
