from   sys        import exit        as SYSEXIT
from   strings    import log         as sLog
from   globalVars import launchTypes as LT
from   excelRW    import Excel
from   tables     import CellTable, TableDict
import stringFuncs    as strF
import libClasses     as lib

# основной класс, запуск проверок
class launchScript():
    def __init__(self, book, type:str, log, errors):    # здесь log и errors – это фреймы
        # запоминаем базовые переменные
        self.type      = type
        self.log       = Log   (log)
        self.errors    = Errors(errors)
        self.fullRange = LT[type]['fullRange']
        self.toTD      = LT[type]['toTD']   # будем работать с TableDict (true) или же с CellTable (false)

        self.getData(book)  # получаем данные
    def getData(self, book):
        self.file     = Excel(book, self.fullRange)
        self.file.table.cutUp(self.searchTitleRow(self.file.table.data))
        self.log       .add  ('readFile',         self.file.table.data)
        if self.toTD:
            self.unkTD = TableDict(self.file.table)
            self.init_curTD()
        else: self.table = CellTable(self.file.table.data)
    def searchTitleRow(self, table:list):   # table – таблица[[]]
        for r in range(len(table)):
            if strF.findSubList(table[r][0], ('Уникальных: ', 'Ошибок: ')) != 0: return r
        return 0
    def init_curTD(self):
        self.curTD = TableDict()
        keys       = [] # ключи[(unkKey,curKey),...], которые потом надо будет переместить из unkTD в curTD

        for libKey, params in lib.columns.data.items():
            unkKey = self.unkTD.searchTitle(params['title'])
            if unkKey is not None:
                self.unkTD.columns[unkKey].title.value = params['title']    # чтобы была правильная капитализация заголовка
                keys.append((unkKey, libKey))

        for item in keys: self.move_fromUnkTD_toCurTD(item[0], item[1])
    def move_fromUnkTD_toCurTD(self, unkKey:str, curKey:str):
        self.curTD.columns[curKey] = self.unkTD.columns.pop(unkKey)

# журнал и ошибки
class Log():    # общие функции классов Log() и Errors()
    def __init__(self, UI): # здесь UI = FRlog/FRerrors (фреймы)
        self.log = []
        self.UI  = UI
    def add(self, type:str, params=None):
        # в params можно передать любые объекты, необходимые для получения доп. данных
        new = self.getType(type, params)
        self. log .append (new)
    def getType(self, type:str, params=None):
        # для Errors() сделать отдельную функцию
        final     = sLog[type]
        if  type == 'readFile':
            rows  = len(params) - 1  # считаем без заголовка
            cols  = len(params[0])
            final = final.replace('%1', str(cols)+' '+strF.getEnding_forCount('столбцы', cols))
            final = final.replace('%2', str(rows)+' '+strF.getEnding_forCount('строки' , rows))
        return final
class Errors(Log):
    def suggest(self):
        pass

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
