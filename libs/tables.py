from sys import exit as SYSEXIT

# надкласс с общими функциями для Table() и CellTable()
class TableTemplate():
   def getSize(self): return len(self.data),len(self.data[0])
   def rotate (self):
      rotated = [[] for cell in self.data[0]]
      for     r  in range(len(self.data)):
         for  c  in range(len(self.data[r])):
            rotated[c].append(self.data[r][c])
      self.data = rotated

# основные классы
class Table(TableTemplate):   # общий класс, можно копировать без изменений в другие программы
   def __init__ (self,values:list,initParams=('toStrings','trimAll')):  # values – таблица[[]]
      self.data       = values
      if 'toStrings' in initParams: self.stringAll()
      if 'trimAll'   in initParams: self.trimAll  ()
   def stringAll(self):
      # конвертирует каждую ячейку таблицы в строку
      for    r in range(len(self.data)):
         for c in range(len(self.data[r])):
            self.data[r][c] = str(self.data[r][c])
   def trimAll  (self):
      # делает .trim() и удаляет плохие символы (напр., мягкие пробелы)
      for    r in range(len(self.data)):
         for c in range(len(self.data[r])):
            self.data[r][c] = self.data[r][c].strip().replace('​','')

# защита от запуска модуля
if __name__ == '__main__':
   print  ("This is module, please don't execute.")
   SYSEXIT()
