import tkinter as tk
from tkinter import ttk
from henryDAO import HenryDAO

#-----------search by author --------
def getTitleCallbackSBA(event):
    nameInd = event.widget.current()
    authNum = auth[nameInd].getAuthNum()
    bookSelectSBA['values'] = dao.getTitlesSBA(authNum)
    bookSelectSBA.current(0)

    bookInd = event.widget.current()
    bookCode = books[bookInd].getCode()
    inventory = dao.getStock(bookCode)
    price = inventory[0].getPrice()
    for i in copiesAvailableSBA.get_children():
        copiesAvailableSBA.delete(i)
    for row in inventory:
        copiesAvailableSBA.insert('','end',values=[row.getBranch(),row.getStock()])

    priceLabSBA = ttk.Label(HenrySBA)
    priceLabSBA.grid(column=1,row=0)
    priceLabSBA['text'] = 'Price: $'+price

def getStockCallbackSBA(event):
    bookInd = event.widget.current()
    bookCode = books[bookInd].getCode()
    inventory = dao.getStock(bookCode)
    price = inventory[0].getPrice()
    for i in copiesAvailableSBA.get_children():
        copiesAvailableSBA.delete(i)
    for row in inventory:
        copiesAvailableSBA.insert('','end',values=[row.getBranch(),row.getStock()])

    priceLabSBA = ttk.Label(HenrySBA)
    priceLabSBA.grid(column=1,row=0)
    priceLabSBA['text'] = 'Price: $'+price

#-----search by category ------

def getCatCallbackSBC(event):
    cat = catSelectSBC.get()
    bookSelectSBC['values'] = dao.getTitlesSBC(cat)
    bookSelectSBC.current(0)

    bookInd = event.widget.current()
    bookCode = books[bookInd].getCode()
    inventory = dao.getStock(bookCode)
    price = inventory[0].getPrice()
    for i in copiesAvailableSBC.get_children():
        copiesAvailableSBC.delete(i)
    for row in inventory:
        copiesAvailableSBC.insert('','end',values=[row.getBranch(),row.getStock()])

    priceLabSBC = ttk.Label(HenrySBC)
    priceLabSBC.grid(column=1,row=0)
    priceLabSBC['text'] = 'Price: $'+price

def getStockCallbackSBC(event):
    bookInd = event.widget.current()
    bookCode = books[bookInd].getCode()
    inventory = dao.getStock(bookCode)
    price = inventory[0].getPrice()
    for i in copiesAvailableSBC.get_children():
        copiesAvailableSBC.delete(i)
    for row in inventory:
        copiesAvailableSBC.insert('','end',values=[row.getBranch(),row.getStock()])

    priceLabSBC = ttk.Label(HenrySBC)
    priceLabSBC.grid(column=1,row=0)
    priceLabSBC['text'] = 'Price: $'+price


#-------search by publisher -------
def getPubCallBack(event):
    pub = pubSelectSBP.get()
    bookSelectSBP ['values'] = dao.getTitleSBP(pub)
    if len(bookSelectSBP['values']) > 0:
        bookSelectSBP.current(0)
        bookInd = event.widget.current()
        bookCode = books[bookInd].getCode()
        inventory = dao.getStock(bookCode)
        price = inventory[0].getPrice()
        for i in copiesAvailableSBP.get_children():
            copiesAvailableSBP.delete(i)
        for row in inventory:
            copiesAvailableSBP.insert('','end',values=[row.getBranch(),row.getStock()])

        priceLabSBP = ttk.Label(HenrySBP)
        priceLabSBP.grid(column=1,row=0)
        priceLabSBP['text'] = 'Price: $'+price
    else:
        bookSelectSBP.set('')
        for i in copiesAvailableSBP.get_children():
            copiesAvailableSBP.delete(i)
        priceLabSBP = ttk.Label(HenrySBP)
        priceLabSBP.grid(column=1,row=0)
        priceLabSBP['text'] = 'Price: None'



def getStockCallbackSBP(event):
    bookInd = event.widget.current()
    bookCode = books[bookInd].getCode()
    inventory = dao.getStock(bookCode)
    price = inventory[0].getPrice()
    for i in copiesAvailableSBP.get_children():
        copiesAvailableSBP.delete(i)
    for row in inventory:
        copiesAvailableSBP.insert('','end',values=[row.getBranch(),row.getStock()])

    priceLabSBP = ttk.Label(HenrySBP)
    priceLabSBP.grid(column=1,row=0)
    priceLabSBP['text'] = 'Price: $'+price

dao = HenryDAO()

books = dao.getBookData()
auth = dao.getAuthorData()
cats = dao.getCatData()
pubs = dao.getPubData()

root = tk.Tk()
root.title('Henry Bookstore')
root.geometry('800x400')

tabControl = ttk.Notebook(root)
HenrySBA = ttk.Frame(tabControl)
HenrySBC = ttk.Frame(tabControl)
HenrySBP = ttk.Frame(tabControl)

tabControl.add(HenrySBA,text='Search by Author')
tabControl.add(HenrySBC,text='Search by Category')
tabControl.add(HenrySBP,text='Search by Publisher')
tabControl.pack(expand = 1, fill ="both")

#---- author
#Change so book select uses book code not title
authSelectSBA = ttk.Combobox(HenrySBA, width=20,state='readonly')
authSelectSBA.grid(column=0,row=2)
authSelectSBA['values'] = [val.getFirst()+' '+val.getLast() for val in auth]
authSelectSBA.current(0)
authSelectSBA.bind('<<ComboboxSelected>>',getTitleCallbackSBA)

authLab = ttk.Label(HenrySBA)
authLab.grid(column=0,row=1)
authLab['text'] = 'Select an author'

titleLabSBA = ttk.Label(HenrySBA)
titleLabSBA.grid(column=1,row=1)
titleLabSBA['text'] = 'Select a title'

bookSelectSBA = ttk.Combobox(HenrySBA, width=20,state='readonly')
bookSelectSBA.grid(column=1,row=2)
bookSelectSBA.bind('<<ComboboxSelected>>',getStockCallbackSBA)

init_authNum = auth[0].getAuthNum()
bookSelectSBA['values'] = dao.getTitlesSBA(init_authNum)
bookSelectSBA.current(0)


copiesAvailableSBA = ttk.Treeview(HenrySBA,columns=('Branch','Copies Available'),show='headings')
copiesAvailableSBA.heading('Branch', text='Branch Name')
copiesAvailableSBA.heading('Copies Available', text='Copies Available')
copiesAvailableSBA.grid(column=0,row=0)
#-----new -- initializing
bookCode = str(books[0].getCode())
inventory = dao.getStock(bookCode)
priceSBA = inventory[0].getPrice()
for i in copiesAvailableSBA.get_children():
    copiesAvailableSBA.delete(i)
for row in inventory:
    copiesAvailableSBA.insert('','end',values=[row.getBranch(),row.getStock()])

priceLabSBA = ttk.Label(HenrySBA)
priceLabSBA.grid(column=1,row=0)
priceLabSBA['text'] = 'Price: $'+priceSBA


#---category

catSelectSBC = ttk.Combobox(HenrySBC, width=20, state='readonly')
catSelectSBC.grid(column=0,row=2)
catSelectSBC['values'] = [val for val in cats]
catSelectSBC.current(0)
catSelectSBC.bind('<<ComboboxSelected>>',getCatCallbackSBC)

catLab = ttk.Label(HenrySBC)
catLab.grid(column=0,row=1)
catLab['text'] = 'Select a Category'

titleLabSBC = ttk.Label(HenrySBC)
titleLabSBC.grid(column=1,row=1)
titleLabSBC['text'] = 'Select a title'

bookSelectSBC = ttk.Combobox(HenrySBC,width=20,state='readonly')
bookSelectSBC.grid(column=1,row=2)
bookSelectSBC.bind('<<ComboboxSelected>>',getStockCallbackSBC)
cat = catSelectSBC.get()
bookSelectSBC['values'] = dao.getTitlesSBC(cat)
bookSelectSBC.current(0)

copiesAvailableSBC = ttk.Treeview(HenrySBC,columns=('Branch','Copies Available'),show='headings')
copiesAvailableSBC.heading('Branch', text='Branch Name')
copiesAvailableSBC.heading('Copies Available', text='Copies Available')
copiesAvailableSBC.grid(column=0,row=0)

bookCode = str(books[0].getCode())
inventory = dao.getStock(bookCode)
priceSBC = inventory[0].getPrice()
for i in copiesAvailableSBC.get_children():
    copiesAvailableSBC.delete(i)
for row in inventory:
    copiesAvailableSBC.insert('','end',values=[row.getBranch(),row.getStock()])

priceLabSBC = ttk.Label(HenrySBC)
priceLabSBC.grid(column=1,row=0)
priceLabSBC['text'] = 'Price: $'+priceSBC

#---publisher

pubSelectSBP = ttk.Combobox(HenrySBP,width=20, state='readonly')
pubSelectSBP.grid(column=0,row=2)
pubSelectSBP['values'] = [pub for pub in pubs]
pubSelectSBP.current(0)
pubSelectSBP.bind('<<ComboboxSelected>>', getPubCallBack)

pubLab = ttk.Label(HenrySBP)
pubLab.grid(column=0,row=1)
pubLab['text'] = 'Select a Category'

titleLabSBC = ttk.Label(HenrySBP)
titleLabSBC.grid(column=1,row=1)
titleLabSBC['text'] = 'Select a title'

bookSelectSBP = ttk.Combobox(HenrySBP,width=20,state='readonly')
bookSelectSBP.grid(column=1,row=2)
bookSelectSBP.bind('<<ComboboxSelected>>',getStockCallbackSBP)
pub = pubSelectSBP.get()
bookSelectSBP ['values'] = dao.getTitleSBP(pub)
if len(bookSelectSBP['values']) > 0:
    bookSelectSBP.current(0)
else:
    bookSelectSBP.set('')

copiesAvailableSBP = ttk.Treeview(HenrySBP,columns=('Branch','Copies Available'),show='headings')
copiesAvailableSBP.heading('Branch', text='Branch Name')
copiesAvailableSBP.heading('Copies Available', text='Copies Available')
copiesAvailableSBP.grid(column=0,row=0)

bookCode = str(books[0].getCode())
inventory = dao.getStock(bookCode)
priceSBP = inventory[0].getPrice()
for i in copiesAvailableSBP.get_children():
    copiesAvailableSBP.delete(i)
for row in inventory:
    copiesAvailableSBP.insert('','end',values=[row.getBranch(),row.getStock()])

priceLabSBP = ttk.Label(HenrySBP)
priceLabSBP.grid(column=1,row=0)
priceLabSBP['text'] = 'Price: $'+priceSBP


root.mainloop()
