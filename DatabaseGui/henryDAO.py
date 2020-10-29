import mysql.connector
from henryInterfaceClasses import Author, Stock, Book

class HenryDAO():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            user='root',
            passwd='monday185',
            database='comp3421',
            host='127.0.0.1')

        self.mycur = self.mydb.cursor()

        def close(self):
            self.mydb.commit()
            self.mydb.close()

    def getAuthorData(self):
        qry = "select distinct a.AUTHOR_NUM,AUTHOR_LAST,AUTHOR_FIRST from henry_author a join henry_wrote w on a.AUTHOR_NUM=w.AUTHOR_NUM"
        self.mycur.execute(qry)

        return [Author(row[0],row[2],row[1]) for row in self.mycur]

    def getTitlesSBA(self, authNum):
        qry = 'select TITLE from henry_book b join henry_wrote w on w.BOOK_CODE = b.BOOK_CODE where AUTHOR_NUM ="'+authNum+'"'
        self.mycur.execute(qry)

        return [row[0] for row in self.mycur]

    def getStock(self,code):
        qry = 'select BRANCH_NAME, ON_HAND, PRICE from henry_inventory i join henry_book b on i.book_code=b.book_code join henry_branch br on br.branch_num = i.branch_num where b.BOOK_CODE = "'+code+'"'
        self.mycur.execute(qry)
        return [Stock(row[0],row[1],row[2]) for row in self.mycur]

    def getCatData(self):
        qry = "select  distinct TYPE from henry_book"
        self.mycur.execute(qry)
        return [row[0] for row in self.mycur]

    def getTitlesSBC(self, cat):
        qry = 'select TITLE from henry_book where TYPE = "'+cat+'"'
        self.mycur.execute(qry)
        return [row[0] for row in self.mycur]

    def getPubData(self):
        qry = 'select distinct PUBLISHER_NAME from henry_publisher p join henry_book b on p.PUBLISHER_CODE=b.PUBLISHER_CODE'
        self.mycur.execute(qry)
        return [row[0] for row in self.mycur]

    def getTitleSBP(self,pub):
        qry = 'select TITLE from henry_book b join henry_publisher p on p.PUBLISHER_CODE=b.PUBLISHER_CODE where PUBLISHER_NAME="'+pub+'"'
        self.mycur.execute(qry)
        return [row[0] for row in self.mycur]

    def getBookData(self):
        qry = 'select book_code,title,type,price from henry_book'
        self.mycur.execute(qry)
        return [Book(row[0],row[1],row[2],row[3]) for row in self.mycur]
