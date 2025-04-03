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
        self.data = {}
        self.mainRead(read,readParams)
    def mainRead(self,type:str,params=('toStrings','trimAll')):
        def readFullSheet(sheet:xw.Sheet): readRange(sheet.used_range)
        def readRange    (range:xw.Range,getAll=False):
            # getAll чтобы прочитать в 'table' весь лист, но в 'addr' и 'range' оставить только изнач. range
            # (нужно для type == 'shSelection')
            def getValues(range:xw.Range):
                return range.options(ndim=2,empty='',numbers=int).value # ndim=2 всегда даёт двумерный массив

            readRange = range.sheet.used_range if getAll else range
            self.data  [range.sheet.name] = {
                'addr' :range.address,
                'range':range,
                'sheet':range.sheet,
                'table':Table(getValues(readRange),params)
                }

        match type:
            case 'shAll'      :
                for sheet in self.file.sheets: readFullSheet(sheet)
            case 'shActive'   : readFullSheet(self.file.sheets.active)
            case 'shSelection': readRange    (self.file.selection,True)
            case   'selection': readRange    (self.file.selection)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
