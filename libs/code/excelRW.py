# Excel read & write
from   sys import exit as SYSEXIT
import datetime        as dt
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
    def __init__(self,book:xw.Book,read='shActive',readParams=('toStrings','trimAll')):
        # read может быть 'selection', 'shActive'(fullRange) или 'shAll'(fullRange)
        # по необходимости можно добавить чтение диапазонов типа 'sheetName:range'
        self.file = book
        self.mainRead(read,readParams)
    def mainRead(self,type:str,params=('toStrings','trimAll')):
        self.data = {}
        if type == 'shAll':
            for sheet in self.file.sheets: self.readFullSheet(sheet,params)
        else:
            sheet      = self.file.sheets.active
            if   type == 'shActive' : self.readFullSheet(sheet,params)
            elif type == 'selection': self.readRange    (sheet.name,self.file.selection,params)
    def readFullSheet(self,sheet:xw.Sheet,params:tuple): self.readRange(sheet.name,sheet.used_range,params)
    def readRange(self,sheetName:str,range:xw.Range,params:tuple):
        self.data[sheetName] = {
            'addr'    :range.address,
            'rangeObj':range,
            'table'   :Table(range.options(ndim=2,empty='',numbers=int).value,params)
            }   # ndim=2 всегда даёт двумерный массив
    def write(self,shName:str,type:str,newSheet=False,saveAfter=False):
        # type может быть 'selection' или 'shActive'(fullRange)
        if type == 'selection':
            print('2')
            self.data[shName]['rangeObj'].value = self.data[shName]['table'].data

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
