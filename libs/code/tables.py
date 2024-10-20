from   sys     import exit as SYSEXIT
from   copy    import deepcopy
import stringFuncs as strF

# функции инициализации
def getCells_fromList(values:list,errors=False):    # errors – значение по умолчанию для всех ячеек
    return [Cell(val,errors) for val in values]

# надкласс с общими функциями для Table() и CellTable()
class TableTemplate():
    def cutUp(self,row:int):
        # обрезать сверху, row останется в итоговой таблице (т. е. row=0 вернёт то же самое)
        self.data = self.data[row:]
    def rotate(self):
        rotated = [[] for cell in self.data[0]]
        for      r  in  range(len(self.data)):
            for  c  in  range(len(self.data[r])):
                rotated[c].append(self.data[r][c])
        self.data = rotated
    def rmEmptyRC(self,type='rc',ignoreTitles=True):
        # type=r/c/rc; ignoreTitles работает только для столбцов
        rows,cols = self.findEmptyRC(type,ignoreTitles)
        self.rmRClist('r',rows)
        self.rmRClist('c',cols)
        return {'rows':rows, 'cols':cols}
    def rmRClist(self,type:str,list:list):          # type = 'r'/'c'
        for i in sorted(list,reverse=True): self.rmRC(type,i)
    def rmRC    (self,type:str,num:int,count=1):    # type = 'r'/'c'
        for counter in range(count):
            if type == 'r':     self.data.pop(num)
            else:
                for row in self.data: row.pop(num)

# основные классы
class Table(TableTemplate): # общий класс, можно копировать без изменений в другие программы
    def __init__(self,values:list,initParams=('toStrings','trimAll')):  # values – таблица[[]]
        self.data = values
        if 'toStrings' in initParams: self.stringAll()
        if 'trimAll'   in initParams: self.trimAll  ()
    def getSize(self): return len(self.data),len(self.data[0])
    def stringAll(self):
        # конвертирует каждую ячейку таблицы в строку
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                self.data[r][c] = str(self.data[r][c])
    def trimAll(self):
        # делает .trim() и удаляет плохие символы (напр., мягкие пробелы)
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                self.data[r][c] = self.data[r][c].strip().replace('​','')
    def findEmptyRC(self,type:str,ignoreTitles:bool):
        # f = final
        table = self.data
        if len(table) > ignoreTitles:
            fRows = []                                  # будем добавлять, если найдём пустую строку
            fCols = [c for c in range(len(table[0]))]   # сначала в списке всё, потом будем удалять непустые

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
            return fRows,fCols
        else: return [],[]
    def equals     (self,tObj):
        # сравнивает эту CellTable (self) с другой CellTable (tObj); вернёт True или False
        this,sec = self.data,tObj.data  # эта и secondary таблицы
        if len(this) != len(sec) or len(this[0]) != len(sec[0]): return False
        for     r in range(len(this)):
            for c in range(len(this[r])):
                if this[r][c] != sec[r][c]: return False
        return True
class CellTable(TableTemplate):
    # общий класс, ВОЗМОЖНО подойдёт для других программ
    # это таблица, в которой каждая ячейка – это объект Cell [[CellObj,...],...]
    def __init__(self,tObj,initCells=True,errors=False):
        # если initCells=True,  в tObj получаем объект Table и создаём внутри объекты CellObj
        # если initCells=False, в tObj получаем массив [[CellObj,...],...]
        # errors – значение по умолчанию для всех ячеек
        self.data = [getCells_fromList(row,errors) for row in tObj.data] if initCells else tObj
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
        self.changed = False    # изменялось ли значение ячейки; важно, например, для вертикалей

# это таблица, представленная в виде словаря {'столбец': TableColumn() obj,...}
class TableDict():
    def __init__(self,tObj:Table=None,errors=False):
        # если tObj=None, создаём пустой объект без колонок; errors – значение по умолчанию для всех ячеек
        self.columns = {}   # основное хранилище столбцов (объектов TableColumn)
        if tObj is not None:
            tObj = deepcopy(tObj)
            tObj    .rotate()
            for r in range(len(tObj.data)):
                self.columns[str(r)] = TableColumn(tObj.data[r],errors,initPos=r)
    def addEmptyColumn(self,key:str,title:str,cellCount:int):
        self.columns[key] = TableColumn(['' for i in range(cellCount)],title=title)

    def searchTitle(self,title:str,fullText=True,lower=True,strip=''):
        for key,column in self.columns.items():
            if strF.findSub(column.title.value,title,'bool',fullText,lower,strip): return key
    def toCellTable(self):
        # получаем "список" позиций и ключей столбцов
        keys = {}
        for key,column in self.columns.items(): keys[str(column.initPos)] = key

        # создаём ротированную CellTable, затем переворачиваем её
        table = []
        for i in sorted([int(key) for key in keys.keys()]):
            column = self.columns[keys[str(i)]]
            table.append([column.title]+column.cells)
        CT = CellTable(table,False)
        CT.rotate()
        return CT
class TableColumn():    # title=CellObj, cells=[CellObj,...]
    def __init__(self,values:list,errors=False,title=None,initPos:int=None):
        if title is None:         title = values.pop(0) # pop удаляет элемент 0 и возвращает его
        self.title   = Cell             (title, errors)
        self.cells   = getCells_fromList(values,errors)
        self.initPos = initPos

        # для вывода в шапке таблицы
        self.unique  = None
        self.errors  = len(values) if errors else 0

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
