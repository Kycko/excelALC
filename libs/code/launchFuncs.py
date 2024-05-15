from sys        import exit        as SYSEXIT
from globalVars import launchTypes as LT
from excelRW    import Excel

class launchScript():
    def __init__(self, book, type, log, errors):
        self.type   = type      # строка
        self.log    = log       # потом заменим на класс Log
        self.errors = errors    # потом заменим на класс Errors
        self.file   = Excel(book, LT[type]['fullRange'])

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
