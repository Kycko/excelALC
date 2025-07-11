# Excel read & write
from   sys import exit as SYSEXIT
import xlwings         as xw
from   globalsMain import dict as Gdict
from   tables      import *

def getCurExcel():
  try:
    book = xw.books.active
    return {'obj'  :book,                     # сама книга (объект из xlwings)
            'file' :book.name,                # название книги
            'sheet':book.sheets.active.name}  # название листа
  except: return None

class Excel():  # общий класс, можно копировать без изменений в другие программы
  # чтение
  def __init__ (self,book:xw.Book,read='shActive',readParams=('toStrings','trimAll')):
    # read может быть 'selection', 'shSelection'(combo), 'shActive'(fullRange) или 'shAll'(fullRange)
    # по необходимости можно добавить чтение диапазонов типа 'sheetName:range'
    self.file = book
    self.data = {}
    self.mainRead(read,readParams)
  def mainRead (self,type:str,params=('toStrings','trimAll')):
    def _fullSheet(sheet:xw.Sheet): _range(sheet.used_range)
    def _range    (range:xw.Range,getAll=False):
      # getAll чтобы прочитать в 'table' весь лист, но в 'addr' и 'range' оставить только изнач. range
      # (нужно для type == 'shSelection')
      readRange = range.sheet.used_range if getAll else range
      self.data  [range.sheet.name] = {
        'addr' :range.address,
        'range':range,
        'sheet':range.sheet,
        'table':Table(self.getValues(readRange),params)
        }

    match type:
      case 'shAll'      :
        for sheet in self.file.sheets: _fullSheet(sheet)
      case 'shActive'   : _fullSheet(self.file.sheets.active)
      case 'shSelection': _range    (self.file.selection,True)
      case   'selection': _range    (self.file.selection)
  def getValues(self,range:xw.Range):
    return range.options(ndim=2,empty='',numbers=int).value # ndim=2 всегда даёт двумерный массив

  # запись; type может быть 'selection' или 'shActive'(fullRange)
  def write        (self,shName:str):
    shObj = self.data[shName]
    shObj['range'].number_format = '@'
    shObj['range'].value         = shObj['table'].data
  def copySheet    (self,shName:str):
    self.data[shName]['sheet'] = self.data[shName]['sheet'].copy()  # возвращает новый лист
  def clearData    (self,shName:str): self.data[shName]['sheet'].clear_contents()
  def resetBgColors(self,shName:str,type:str):
    if type != 'none':
      shObj  =  self.data[shName]
      match type:
        case 'sh'      : rng = shObj['sheet'].used_range
        case 'sel'     : rng = shObj['range']
        case 'firstRow':
          lastCol = shObj['range'].columns.count
          rng     = shObj['sheet'].range((1,1),(1,lastCol))
      rng.color = None
  def setCellColor (self,shName:str,type:str,row:int,col:int,color:str):
    shObj      = self.data[shName]
    match type:
      case 'selection':
        # f = first
        fCol,fRow = self.cellNums_fromAddr(shObj['addr'].split(':')[0])
        cell      = shObj['sheet'][fRow+row,fCol+col]
      case 'shActive' : cell = shObj['sheet'][row,col]
    cell.color = color
  def rmRCrange    (self,shName:str,type:str,rng:dict): # rng={from:int,to:int}
    match type:
      case 'rows': s,f = str(rng['from']+1),str(rng['to']+1)
      case 'cols':
        s = self.colInt_toLetter(rng['from'])
        f = self.colInt_toLetter(rng['to'])
    self.data[shName]['sheet'].range(s+':'+f).delete()
  def save(self):   self.file.save()

  # оформление
  def pinTitle(self,shName:str,row:int):
    self.data[shName]['sheet'][row+1,0].select()
    self.callPin(True)
  def callPin (self,state :bool): self.file.app.api.ActiveWindow.FreezePanes = state
  def filter  (self,state :bool ,obj=None):
    # obj=xw.Range, чтобы установить фильтр, и =xw.Sheet, чтобы удалить его с листа
    match state:
      case  True: obj.api.AutoFilter(Field:=1)
      case False: obj.api.AutoFilterMode = False

  # вспомогательные
  def splitCellAddr    (self,addr:str):
    return (''.join(filter(str.isalpha,addr)) or None,
            ''.join(filter(str.isdigit,addr)) or None)
  def colLetters_toInt (self,letters:str):  # преобразует, например, 'AC' в 29
    lib,final = Gdict.colLetters,0
    for symb in letters: final += lib.find(symb)
    return final
  def colInt_toLetter  (self,num    :int):  # преобразует, например,  3 в  'C'
    startIndex,final = 1,'' # it can start either at 0 or at 1
    while num > 25+startIndex:
      temp   = int((num-startIndex)/26)
      final += chr (64 +temp)
      num   -= temp*26
    final += chr(65-startIndex+(num))
    return final
  def cellNums_fromAddr(self,cell:str):
    col,row = self.splitCellAddr  (cell)
    return   (self.colLetters_toInt(col),int(row)-1)

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
