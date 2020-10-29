Author: Ben Tennant

This project is a GUI to access the fictional Henry Bookstore database. It is written in python
using tkinter and embedded SQL to access the database. It offers three options to search for a book:
search by author, category(genre) or publisher. From there the user can select a title and the interface
will provide the price of the book and each store that currently has the title in stock and the stock
available for each store location. The HenryDAO is the data access object file that contains a class that 
performs all the queries seperate from the GUI. As anyone reading thiscannot access the database I used, 
I have included the SQL script to create the database if one would like to test it.