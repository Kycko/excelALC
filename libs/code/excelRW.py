# Excel read & write
from   sys import exit as SYSEXIT
import xlwings         as xw
from   tables      import *

class exBooks():    # Excel books
    def update(self):
        self.books     = []
        self.bookNames = []

        try:
            self.cur  = xw.books.active.name
            for book in xw.books:
                self.books    .append(book)
                self.bookNames.append(book.name)
        except: self.cur = ''
    def getFile(self,file:str):
        self.update()
        for book in self.books:
            if book.name == file: return book
        return None

class Excel():  # общий класс, можно копировать без изменений в другие программы
    def __init__(self,book:xw.Book,fullRange=True):
        # если fullRange=False, считываем выделенный диапазон
        self.file  = book
        self.sheet = book.sheets.active
        self.range = None if fullRange else book.selection
        self.read()
    def getRange(self):
        # вернёт либо used_range (весь диапазон с данными), либо выбранный диапазон
        return self.sheet.used_range if self.range is None else self.range
    def read(self):
        self.dataRange = self.getRange()                                        # нужен в т. ч. для лога
        self.table     = Table(self.dataRange.options(ndim=2,empty='').value)   # ndim=2 всегда даёт двумерный массив
        self.table.stringAll  ()
        self.table.trimAll    ()

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
