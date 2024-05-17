from sys  import exit as SYSEXIT
from copy import deepcopy

# функции инициализации
def getCells_fromList(values:list, errors=False):   # errors – значение по умолчанию для всех ячеек
    return [Cell(val, errors) for val in values]

# надкласс с общими функциями для Table() и CellTable()
class TableTemplate():
    def cutUp(self, row:int):
        # обрезать сверху, row останется в итоговой таблице (т. е. row=0 вернёт то же самое)
        self.data = self.data[row:]
    def rotate(self):
        rotated = [[] for cell in self.data[0]]
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                rotated[c].append(self.data[r][c])
        self.data = rotated

# основные классы
class Table(TableTemplate):             # общий класс, можно копировать без изменений в другие программы
    def __init__(self, values:list):    # values – таблица[[]]
        self.data = values
class CellTable(TableTemplate):
    # общий класс, ВОЗМОЖНО подойдёт для других программ
    # это таблица, в которой каждая ячейка – это словарь [[{value:'', error:true/false}, ...], ...]
    def __init__(self, table:list, errors=False):  # table – таблица[[]], errors – значение по умолчанию для всех ячеек
        self.data = [getCells_fromList(row, errors) for row in table]
class Cell():
    def __init__(self, value, error=False):
        self.value = value
        self.error = error

# это таблица, представленная в виде словаря {столбец: {title:CellObj, cells:[CellObj,...]},...}
class TableDict():
    def __init__(self, tObj:Table, errors=False):  # errors – значение по умолчанию для всех ячеек
        self.columns = {}
        tObj = deepcopy(tObj)
        tObj.rotate()
        for r in range(len(tObj.data)):
            self.columns[str(r)] = TableColumn(tObj.data[r], errors)
class TableColumn():
    def __init__(self, values:list, errors=False, title:str=None):
        if title == None: title = values.pop(0) # pop удаляет элемент 0 и возвращает его
        self.title = Cell             (title,  errors)
        self.cells = getCells_fromList(values, errors)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
