from sys import exit as SYSEXIT

class Table():  # общий класс, можно копировать без изменений в другие программы
    def __init__(self, values:list):    # values – таблица [[]]
        self.data = values
        self.size = {'rows': len(values), 'cols': len(values[0])}

class CellTable():
    # общий класс, ВОЗМОЖНО подойдёт для других программ
    # это таблица, в которой каждая ячейка – это словарь [[{value:'', error:true/false}, ...], ...]
    def __init__(self, table:Table):
        pass

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
