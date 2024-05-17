from   sys        import exit        as SYSEXIT
from   globalVars import launchTypes as LT
from   excelRW    import Excel
from   tables     import CellTable, TableDict
import stringFuncs    as strF

class launchScript():
    def __init__(self, book, type:str, log, errors):
        # запоминаем базовые переменные
        self.type      = type
        self.log       = log                # потом заменим на класс Log
        self.errors    = errors             # потом заменим на класс Errors
        self.fullRange = LT[type]['fullRange']
        self.toTD      = LT[type]['toTD']   # будем работать с TableDict (true) или же с CellTable (false)

        # создаём объекты для последующей обработки
        self.file     = Excel(book, self.fullRange)
        self.file.table.cutUp(self.searchTitleRow(self.file.table.data))
        if self.toTD: self.unkTD = TableDict     (self.file.table)
        else:         self.table = CellTable     (self.file.table.data)
    def searchTitleRow(self, table):
    def searchTitleRow(self, table:list):   # values – таблица[[]]
        for r in range(len(table)):
            if strF.findSubList(table[r][0], ('Уникальных: ', 'Ошибок: ')) != 0: return r
        return 0

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
