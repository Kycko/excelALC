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
    # чтение
    def __init__(self,book:xw.Book,read='shActive',readParams=('toStrings','trimAll')):
        # read может быть 'selection', 'shActive'(fullRange) или 'shAll'(fullRange)
        # по необходимости можно добавить чтение диапазонов типа 'sheetName:range'
        self.file = book
        self.mainRead(read,readParams)
    def mainRead(self,type:str,params=('toStrings','trimAll')):
        self.data = {}
        if   type == 'shAll'    :
            for sheet in self.file.sheets: self.readFullSheet(sheet,params)
        elif type == 'shActive' : self.readFullSheet(self.file.sheets.active,params)
        elif type == 'selection': self.readRange    (self.file.selection    ,params)
    def readFullSheet(self,sheet:xw.Sheet,params:tuple): self.readRange(sheet.used_range,params)
    def readRange(self,range:xw.Range,params:tuple):
        self.data[range.sheet.name] = {
            'addr' :range.address,
            'range':range,
            'sheet':range.sheet,
            'table':Table(range.options(ndim=2,empty='',numbers=int).value,params)
            }   # ndim=2 всегда даёт двумерный массив

    # запись; type может быть 'selection' или 'shActive'(fullRange)
    def write(self,shName:str,type:str,newSheet=False):
        shObj = self.data[shName]
        if type == 'selection':
            if newSheet:
                # sheet.copy() возвращает новый лист
                shObj['range']   = shObj['sheet'].copy().range(shObj['addr'])
                shObj['sheet']   = shObj['range'].sheet
            shObj['range'].value = shObj['table'].data
        elif type == 'shActive':
            if newSheet: 
    def resetSheetBgColors(self,shName:str): self.data[shName]['sheet'].used_range.color = None
    def setCellColor(self,type:str,shName:str,row:int,col:int,color:str):
        shObj   = self.data[shName]
        if type == 'selection':
            # f = first
            fCol,fRow = self.cellNums_fromAddr(shObj['addr'].split(':')[0])
            shObj['sheet'][fRow+row,fCol+col].color = color
    def save(self): self.file.save()

    # вспомогательные
    def splitCellAddr    (self,addr   :str):
        return (''.join(filter(str.isalpha,addr)) or None,
                ''.join(filter(str.isdigit,addr)) or None)
    def colLetters_toInt (self,letters:str):
        # преобразует, например, 'AC' в 29
        lib   = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        final = 0
        for symb in letters: final += lib.find(symb)
        return final
    def cellNums_fromAddr(self,cell   :str):
        col,row = self.splitCellAddr  (cell)
        return   (self.colLetters_toInt(col), int(row)-1)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
