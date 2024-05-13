# Excel read & write
from   sys import exit as SYSEXIT
import xlwings         as xw

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

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
