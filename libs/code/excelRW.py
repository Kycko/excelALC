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
        if newSheet:
            shObj['sheet'] = shObj['sheet'].copy()  # возвращает новый лист
            if   type == 'selection': shObj['range'] = shObj['sheet'].range(shObj['addr'])
            elif type == 'shActive' :
                rows  = len(shObj['table'].data)
                cols  = len(shObj['table'].data[0])
                shObj['range'] = shObj['sheet'].range((1,1),(rows,cols))
                shObj['addr']  = shObj['range'].address
        if type == 'shActive':   shObj['sheet'].clear_contents()
        shObj['range'].value   = shObj['table'].data
    def resetBgColors(self,shName:str,type:str):
        if   type  == 'sheet'    : range = self.data[shName]['sheet'].used_range
        elif type  == 'selection': range = self.data[shName]['range']
        elif type  == 'firstRow' :
            lastCol = self.data[shName]['range'].columns.count
            range   = self.data[shName]['sheet'].range((1,1),(1,lastCol))
        range.color = None
    def setCellColor(self,type:str,shName:str,row:int,col:int,color:str):
        shObj      = self.data[shName]
        if   type == 'selection':
            # f = first
            fCol,fRow = self.cellNums_fromAddr(shObj['addr'].split(':')[0])
            cell = shObj['sheet'][fRow+row,fCol+col]
        elif type == 'shActive': cell = shObj['sheet'][row,col]
        cell.color = color
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
