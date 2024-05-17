from sys        import exit        as SYSEXIT
from globalVars import launchTypes as LT
from excelRW    import Excel
from tables     import CellTable, TableDict

class launchScript():
    def __init__(self, book, type:str, log, errors):
        # запоминаем базовые переменные
        self.type      = type
        self.log       = log       # потом заменим на класс Log
        self.errors    = errors    # потом заменим на класс Errors
        self.fullRange = LT[type]['fullRange']
        self.toTD      = LT[type]['toTD']   # будем работать с TableDict (true) или же с CellTable (false)

        # создаём объекты для последующей обработки
        self.file                = Excel(book, self.fullRange)
        if self.toTD: self.table = TableDict  (self.file.table)
        else:         self.table = CellTable  (self.file.table)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
