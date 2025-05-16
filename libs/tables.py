from sys import exit as SYSEXIT

# функции инициализации
def getCells_fromList(values:list,errors=False):
  # errors = значение по умолчанию для всех ячеек
  return [Cell(val,errors) for val in values]

# надкласс с общими функциями для Table() и CellTable()
class TableTemplate():
  def getSize(self): return len(self.data),len(self.data[0])
  def cutUp  (self,row:int):
    # обрезать сверху, row останется в итоговой таблице (т. е. row=0 вернёт то же самое)
    self.data = self.data[row:]
  def rotate (self):
    rotated = [[] for cell in self.data[0]]
    for   r  in range(len(self.data)):
      for c  in range(len(self.data[r])):
        rotated[c].append(self.data[r][c])
    self.data = rotated

# основные классы
class     Table(TableTemplate):
  # общий класс, можно копировать без изменений в другие программы
  def __init__   (self,values:list,initParams=('toStrings','trimAll')): # values – таблица[[]]
    self.data       = values
    if 'toStrings' in initParams: self.stringAll()
    if 'trimAll'   in initParams: self.trimAll  ()
  def stringAll  (self):
    # конвертирует каждую ячейку таблицы в строку
    for   r in range(len(self.data)):
      for c in range(len(self.data[r])):
        self.data[r][c] = str(self.data[r][c])
  def trimAll    (self):
    # делает .trim() и удаляет плохие символы (напр., мягкие пробелы)
    for   r in range(len(self.data)):
      for c in range(len(self.data[r])):
        self.data[r][c] = self.data[r][c].strip().replace('​','')
  def findEmptyRC(self,type:str,ignoreTitles:bool):
    # f = final
    # проще считать всё, но возвращать только в зависимости от type=r/c/rc
    table = self.data
    if len(table) > ignoreTitles:
      fRows = []                                # будем добавлять, если найдём пустую строку
      fCols = [c for c in range(len(table[0]))] # сначала в списке всё, потом будем удалять непустые

      for r in range(ignoreTitles,len(table)):
        emptyRow     = True
        nonEmptyCols = []
        for c in range(len(table[r])):
          if table[r][c]:
            emptyRow = False
            nonEmptyCols.append(c)

        if emptyRow: fRows.append(r)
        for col in nonEmptyCols:
          if col in fCols: fCols.remove(col)

      if 'r' not in type: fRows = []
      if 'c' not in type: fCols = []
      return fRows,fCols
    else: return [],[]
  def equals     (self,tObj):
    # сравнивает эту Table(self) с другой Table(tObj); вернёт True или False
    this,sec = self.data,tObj.data  # эта и secondary таблицы
    if len(this) != len(sec) or len(this[0]) != len(sec[0]): return False
    for   r in range(len(this)):
      for c in range(len(this[r])):
        if this[r][c] != sec[r][c]: return False
    return True
class CellTable(TableTemplate):
  # общий класс, ВОЗМОЖНО подойдёт для других программ
  # это таблица, в которой каждая ячейка – это объект Cell [[CellObj,...],...]
  def __init__   (self,tObj,initCells=True,errors=False):
    # если initCells=True,  в tObj получаем объект Table и создаём внутри объекты CellObj
    # если initCells=False, в tObj получаем массив [[CellObj,...],...]
    # errors – значение по умолчанию для всех ячеек
    def _initCells(): return [getCells_fromList(row,errors) for row in tObj.data]
    self.data = _initCells() if initCells else tObj
  def toTable    (self):
    final = []
    for row in self.data:
      final.append([])
      for cell in row: final[-1].append(cell.value)
    return Table(final,())
  def findEmptyRC(self,type:str,ignoreTitles:bool): return self.toTable().findEmptyRC(type,ignoreTitles)
class Cell():
  def __init__(self,value,error=False):
    self.value   = value
    self.error   = error
    self.changed = False  # изменялось ли значение ячейки; важно, например, для вертикалей

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
