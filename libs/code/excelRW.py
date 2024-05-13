# Excel read & write
from   sys import exit as SYSEXIT
import xlwings         as xw
from   tables      import *

class exBooks():    # Excel books
    def __init__(self):
        pass
    def update(self):
        self.books     = []
        self.bookNames = []
        if xw.apps.count and xw.books.count:
            for book in xw.books:
                self.books    .append(book)
                self.bookNames.append(book.name)

        try:    self.cur = xw.books.active.name
        except: self.cur = ''
    def getFile(self, file):
        self.update()
        for book in self.books:
            if book.name == file: return book
        return None

class Excel():  # общий класс, можно копировать без изменений в другие программы
    def __init__(self, book, fullRange=True):
        # если fullRange=False, считываем выделенный диапазон
        self.file  = book
        self.sheet = book.sheets.active
        self.range = None if fullRange else book.selection
        self.read()
    def getRange(self):
        # вернёт либо used_range (весь диапазон с данными), либо выбранный диапазон
        return self.sheet.used_range if self.range is None else self.range
    def read(self):
        self.table = Table(self.getRange().options(ndim=2).value)   # ndim=2 позволяет всегда получать двумерный массив

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
