from sys import exit as SYSEXIT

class Table():  # общий класс, можно копировать без изменений в другие программы
    def __init__(self, values):
        self.data = values
        self.size = {'rows': len(values), 'cols': len(values[0])}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
