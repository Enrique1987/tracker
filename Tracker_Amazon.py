# -*- coding: utf-8 -*-
"""
Updated: February 11, 2025
@author: Enrique Benito Casado
@Email: enriquebenito1987@gmail.com
"""

import sqlite3
import requests
import smtplib
from bs4 import BeautifulSoup
from tkinter import Tk, Frame, Menu, Label, Entry, Text, Button, Scrollbar, messagebox, StringVar, IntVar, END

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
DB_NAME = "Elementos.db"

# -------------------- Database Functions ---------------------- #

def connect_db():
    """Create database and table if not exists."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TRACKER (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    MESSAGE_SEND INTEGER DEFAULT 0,
                    NAME TEXT,
                    LINK TEXT,
                    PRICE REAL,
                    COMMENT TEXT
                )
            ''')
        messagebox.showinfo("Database", "Connected successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def execute_query(query, params=()):
    """Helper function to execute database queries."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return None

# -------------------- Application Functions ---------------------- #

def clean_fields():
    miName.set("")
    miLink.set("")
    miPrice.set("")
    textoComment.delete(1.0, END)


def create():
    execute_query("""
        INSERT INTO TRACKER (NAME, LINK, PRICE, COMMENT)
        VALUES (?, ?, ?, ?)""", (miName.get(), miLink.get(), miPrice.get(), textoComment.get("1.0", END).strip()))
    messagebox.showinfo("Success", "Record inserted successfully!")
    clean_fields()


def read():
    records = execute_query("SELECT * FROM TRACKER WHERE NAME = ?", (miName.get(),))
    if records:
        miName.set(records[0][2])
        miLink.set(records[0][3])
        miPrice.set(records[0][4])
        textoComment.insert(1.0, records[0][5])
    else:
        messagebox.showwarning("Warning", "No record found!")


def update():
    execute_query("""
        UPDATE TRACKER SET NAME = ?, LINK = ?, PRICE = ?, COMMENT = ?
        WHERE NAME = ?""", (miName.get(), miLink.get(), miPrice.get(), textoComment.get("1.0", END).strip(), miName.get()))
    messagebox.showinfo("Success", "Record updated successfully!")
    clean_fields()


def delete():
    execute_query("DELETE FROM TRACKER WHERE NAME = ?", (miName.get(),))
    messagebox.showinfo("Success", "Record deleted successfully!")
    clean_fields()


def show_all():
    records = execute_query("SELECT NAME, PRICE FROM TRACKER")
    result = "\n".join(f"Name: {rec[0]}, Desired Price: {rec[1]}" for rec in records)
    messagebox.showinfo("Tracked Items", result or "No records found!")

# -------------------- Price Tracking ---------------------- #

def check_price(name, link, desired_price):
    try:
        page = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(page.content, "lxml")
        price_text = soup.find("span", class_="a-size-base a-color-price a-color-price").get_text()
        converted_price = float(price_text.replace(",", ".").split()[0])
        
        if converted_price < float(desired_price):
            messagebox.showinfo("Price Alert", f"{name} is now {converted_price}€! Email sent.")
            send_mail(name, converted_price, link)
        else:
            messagebox.showinfo("Tracking", f"{name} is still above {desired_price}€.")
    except Exception as e:
        messagebox.showerror("Error", f"Price tracking failed: {e}")


def send_mail(article, price, link):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("your-email@gmail.com", "your-app-password")
        subject = "Price Drop Alert!"
        body = f"{article} is now {price}€! Check the link: {link}"
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail("your-email@gmail.com", "recipient-email@gmail.com", message)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email failed: {e}")

# -------------------- UI Setup ---------------------- #
root = Tk()
root.title("Price Tracker")

menu = Menu(root)
root.config(menu=menu)

db_menu = Menu(menu, tearoff=0)
db_menu.add_command(label="Connect", command=connect_db)
db_menu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="Database", menu=db_menu)

frame = Frame(root)
frame.pack()

miName = StringVar()
miPrice = StringVar()
miLink = StringVar()

Label(frame, text="Item Name:").grid(row=0, column=0)
Entry(frame, textvariable=miName).grid(row=0, column=1)

Label(frame, text="Link:").grid(row=1, column=0)
Entry(frame, textvariable=miLink).grid(row=1, column=1)

Label(frame, text="Desired Price:").grid(row=2, column=0)
Entry(frame, textvariable=miPrice).grid(row=2, column=1)

Label(frame, text="Comments:").grid(row=3, column=0)
textoComment = Text(frame, width=25, height=5)
textoComment.grid(row=3, column=1)

Button(frame, text="Create", command=create).grid(row=4, column=0)
Button(frame, text="Read", command=read).grid(row=4, column=1)
Button(frame, text="Update", command=update).grid(row=5, column=0)
Button(frame, text="Delete", command=delete).grid(row=5, column=1)
Button(frame, text="Show All", command=show_all).grid(row=6, column=0, columnspan=2)

root.mainloop()
