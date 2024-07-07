from   sys import exit as SYSEXIT
from   globalFuncs import write_toFile
import globalVars      as G
import appUI
from   excelRW     import Excel
from   tables      import CellTable,TableDict
import strings         as S
import stringFuncs     as strF
import libClasses      as lib

# корневой класс: из него запускаются UI и код других модулей
class Root():
    def __init__(self):
        if lib.ready:
            self.UI = appUI.Window(self)
            self.UI.mainloop()
        else: appUI.cantReadLib()
    # основные функции
    def launch(self,book,type:str):
        # book – это сам объект книги из xlwings; type = например, 'checkEmails'
        params = G.launchTypes[type]

        # запоминаем базовые переменные
        self.type       = type
        self.errors     = Errors(self.UI.errors)
        self.log        = Log   (self.UI)
        self.log.add('launch',type)
        self.fullRange  = params['fullRange']
        self.toTD       = params['toTD'] # будем работать с TableDict (True) или же с CellTable (False)
        self.justVerify = params['justVerify']
        if params['getSuggParam']: self.suggErrors = G.config.get(type + ':suggestErrors')

        self.getData(book)  # получаем данные
        #if params['launch'] == 'rangeChecker': self.rangeChecker(self.table.data, params['AStype']) # проверяем выделенный диапазон

    # чтение данных из таблицы
    def getData(self,book): # book – это сам объект книги из xlwings
        self.file     = Excel(book,self.fullRange)
        self.file.table.cutUp(self.searchTitleRow(self.file.table.data))
        self.log .add('readSheet',         self.file.sheet.name)
        self.log .add('readFile' ,{'table':self.file.table.data,
                                   'range':self.fullRange,
                                   'addr' :self.file.dataRange.address})

        if self.toTD:
            self.unkTD = TableDict(self.file.table)
            self.init_curTD()
        else: self.table = CellTable(self.file.table.data)
    def searchTitleRow(self,table:list):    # table = таблица[[]]
        for r in range(len(table)):
            if strF.findSubList(table[r][0],('Уникальных: ','Ошибок: '),'index') != 0: return r
        return 0
    def init_curTD(self):
        self.curTD = TableDict()
        keys       = [] # ключи[(unkKey,curKey),...], которые потом надо будет переместить из unkTD в curTD

        for libKey,params in lib.columns.data.items():
            unkKey = self.unkTD.searchTitle(params['title'])
            if unkKey is not None:
                self.unkTD.columns[unkKey].title.value = params['title']    # чтобы была правильная капитализация заголовка
                keys.append((unkKey,libKey))

        for item in keys: self.move_fromUnkTD_toCurTD(item[0],item[1])
    def move_fromUnkTD_toCurTD(self,unkKey:str,curKey:str):
        self.curTD.columns[curKey] = self.unkTD.columns.pop(unkKey)

# журнал и ошибки
class Log():
    def __init__(self,UI:appUI.Window):
        self.UI   = UI
        self.file = G.files['log']
        write_toFile([],self.file)
    def add(self,type:str,params=None):
        # в params можно передать любые объекты, необходимые для получения доп. данных
        new  = self.getType(type,params)
        write_toFile(new,self.file,True)
        self.UI.log (new)
    def getType(self,type:str,params=None):
        if   type == 'launch'   : final = '[core] ' + S.layout['actions'][params]['log']
        elif type == 'readSheet': final = S.log[type].replace('$$1',params)
        elif type == 'readFile':
            final = S.log[type]['full' if params['range'] else 'range']
            rows  = len(params ['table']) - 1*(params['range']) # считаем без заголовка
            cols  = len(params ['table'][0])
            final = final.replace('$$1',params['addr'])
            final = final.replace('$$2',str(cols)+' '+strF.getEnding_forCount(S.words_byCount['столбцы'],cols))
            final = final.replace('$$3',str(rows)+' '+strF.getEnding_forCount(S.words_byCount['строки' ],rows))
        elif type == 'ACsuccess':
            final = S.log[type].replace('$$1',params['type'])
            final = final      .replace('$$2',params['from'])
            final = final      .replace('$$3',params['to'])
        elif type == 'errorsFound':
            final = S.log[type].replace('$$1',params['type']).replace('$$2',str(params['count']))
        return final
class Errors():
    def __init__(self,UI):  # UI = класс appUI.Errors()
        self.storage = {}   # {type:{initLow:ErrorObj,...},...}
        self.UI      = UI
        self.file    = G.files['errors']
        write_toFile([],self.file)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
