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
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                rotated[c].append(self.data[r][c])
        self.data = rotated

# основные классы
class Table(TableTemplate): # общий класс, можно копировать без изменений в другие программы
    def __init__(self,values:list,initParams=('toStrings','trimAll')):  # values – таблица[[]]
        self.data = values
        if 'toStrings' in initParams: self.stringAll()
        if 'trimAll'   in initParams: self.trimAll  ()
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
class CellTable(TableTemplate):
    # общий класс, ВОЗМОЖНО подойдёт для других программ
    # это таблица, в которой каждая ячейка – это объект Cell [[CellObj,...],...]
    def __init__(self,tObj:Table,errors=False): # errors – значение по умолчанию для всех ячеек
        self.data = [getCells_fromList(row,errors) for row in tObj.data]
    def toTable(self):
        final = []
        for row in self.data:
            final.append([])
            for cell in row: final[-1].append(cell.value)
        return Table(final,())
class Cell():
    def __init__(self,value,error=False):
        self.value = value
        self.error = error

# это таблица, представленная в виде словаря {столбец: {title:CellObj, cells:[CellObj,...]},...}
class TableDict():
    def __init__(self,tObj:Table=None,errors=False):
        # если tObj=None, создаём пустой объект без колонок; errors – значение по умолчанию для всех ячеек
        self.columns = {}   # основное хранилище столбцов (объектов TableColumn)
        if tObj is not None:
            tObj = deepcopy(tObj)
            tObj.rotate()
            for r in range(len(tObj.data)):
                self.columns[str(r)] = TableColumn(tObj.data[r],errors,initPos=r)
    def searchTitle(self,title:str,fullText=True,lower=True):
        for key,column in self.columns.items():
            if strF.findSub(column.title.value,title,'bool',fullText,lower): return key
class TableColumn():
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
