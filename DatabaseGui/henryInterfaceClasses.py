class Author():
    def __init__(self,num,first,last):
        self.num = num
        self.first = first
        self.last = last

    def getFirst(self):
        return self.first

    def getLast(self):
        return self.last

    def getAuthNum(self):
        return str(self.num)

class Stock():
    def __init__(self, branch, quantity, price,):
        self.branch = branch
        self.quantity = quantity
        self.price = price

    def getBranch(self):
        return self.branch

    def getStock(self):
        return self.quantity

    def getPrice(self):
        return str(self.price)

class Book():
    def __init__(self,code,title,type,price):
        self.code = code
        self.title = title
        self.type = type
        self.price = price

    def getCode(self):
        return self.code

    def getTitle(self):
        return self.title

    def getType(self):
        return self.type

    def getPrice(self):
        return self.price
