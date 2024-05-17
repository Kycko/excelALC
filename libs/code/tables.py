from sys  import exit as SYSEXIT
from copy import deepcopy

def getCells_fromList(values:list, errors=False):   # errors – значение по умолчанию для всех ячеек
    return [{'value':val, 'error':errors} for val in values]

# надкласс с общими функциями для Table() и CellTable()
class TableTemplate():
    def rotate(self, saveRotated=False):
        # если saveRotated=True, сохранить результат в self.data, иначе только вернуть результат в return
        rotated = [[] for cell in self.data]
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                rotated[c].append(self.data[r][c])

        if saveRotated: self.data = rotated
        return deepcopy(rotated)    # deepcopy на случай, если в ячейках таблицы другие объекты

# основные классы
class Table(TableTemplate):             # общий класс, можно копировать без изменений в другие программы
    def __init__(self, values:list):    # values – таблица[[]]
        self.data = values
    def rotate(self, saveRotated=False):
        return Table(super().rotate(saveRotated))
class CellTable(TableTemplate):
    # общий класс, ВОЗМОЖНО подойдёт для других программ
    # это таблица, в которой каждая ячейка – это словарь [[{value:'', error:true/false}, ...], ...]
    def __init__(self, table:Table, errors=False):  # errors – значение по умолчанию для всех ячеек
        self.data = [getCells_fromList(row, errors) for row in table.data]
    def rotate(self, saveRotated=False):
        # алгоритм выстроен так, чтобы не терять значения errors
        new      = CellTable(Table([[]]))
        new.data = super().rotate(saveRotated)
        return new
class TableDict():
    # общий класс, ВОЗМОЖНО подойдёт для других программ
    # это таблица, представленная в виде словаря {столбец: {title:CellObj, cells:[CellObj,...]},...}
    def __init__(self, table:Table, errors=False):  # errors – значение по умолчанию для всех ячеек
        rotated = table.rotate()


# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
