# Excel read & write
from   sys import exit as SYSEXIT
import xlwings         as xw
from   tables      import *

class Excel():  # общий класс, можно копировать без изменений в другие программы
    # чтение
    def __init__(self,book:xw.Book,read='shActive',readParams=('toStrings','trimAll')):
        # read может быть 'selection', 'shSelection'(combo), 'shActive'(fullRange) или 'shAll'(fullRange)
        # по необходимости можно добавить чтение диапазонов типа 'sheetName:range'
        self.file = book
        self.mainRead(read,readParams)
    def mainRead(self,type:str,params=('toStrings','trimAll')):
        self.data = {}
        if   type == 'shAll'      :
            for sheet in self.file.sheets: self.readFullSheet(sheet,params)
        elif type == 'shActive'   : self.readFullSheet(self.file.sheets.active,params)
        elif type == 'shSelection': self.readRange    (self.file.selection    ,params,True)
        elif type == 'selection'  : self.readRange    (self.file.selection    ,params)
    def readFullSheet(self,sheet:xw.Sheet,params:tuple): self.readRange(sheet.used_range,params)
    def readRange(self,range:xw.Range,params:tuple,getAll=False):
        # getAll позволяет прочитать в 'table' весь лист, но оставить в 'addr' и 'range' только переданный range
        # (нужно для type == 'shSelection')
        readRange = range.sheet.used_range if getAll else range
        self.data[range.sheet.name] = {
            'addr' :range.address,
            'range':range,
            'sheet':range.sheet,
            'table':Table(self.getValues(readRange),params)
            }   # ndim=2 всегда даёт двумерный массив
    def getValues(self,range:xw.Range): return range.options(ndim=2,empty='',numbers=int).value

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
