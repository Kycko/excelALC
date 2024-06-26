from   sys         import exit as SYSEXIT
from   excelRW     import Excel
from   tables      import CellTable, TableDict
from   globalFuncs import write_toFile
import globalVars      as G
import strings         as S
import stringFuncs     as strF
import listFuncs       as listF
import libClasses      as lib

# основной класс, запуск проверок
class launchScript():
    def __init__(self, app, book, type:str, log, errors):    # здесь log и errors – это фреймы
        params = G.launchTypes[type]

        # запоминаем базовые переменные
        self.app        = app   # для вызова функций основного окна
        self.type       = type
        self.log        = Log(log)
        self.log.add    ('launch', type)
        self.errors     = Errors(errors)
        self.fullRange  = params['fullRange']
        self.toTD       = params['toTD'] # будем работать с TableDict (true) или же с CellTable (false)
        self.justVerify = params['justVerify']
        if params['getSuggParam']: self.suggErrors = G.config.get(type + ':suggestErrors')

        self.getData(book)  # получаем данные
        if params['launch'] == 'rangeChecker': self.rangeChecker(self.table.data, params['AStype']) # проверяем выделенный диапазон

    # основные алгоритмы проверки
    def rangeChecker(self, table, type):
        # в table передаём либо CellTable().data, либо [cells[]] из TableColumn
        # т. е. table – это всегда [[Cell,...],...]
        errors = {} # {'initValue'.lower():ErrorObj,...}

        # autocorr и поиск всех ошибок
        for r in range(len(table)):
            for c in range(len(table[r])):
                cell    = table[r][c]
                tempVal = cell.value
                if not self.justVerify: tempVal = self.autocorr(type, tempVal)

                VAL = self.validate_andCapitalize(type, tempVal)
                if VAL['valid'] and not self.justVerify: cell.value = VAL['value']
                else:
                    low = cell.value.lower()
                    if low in errors.keys (): errors[low]  .addPos  (r,c)
                    else:                     errors[low] = ErrorObj(cell.value, r, c)
        if errors: self.errors.add(errors, type)

        # предложение исправить вручную и запись исправлений
        if self.suggErrors: self.suggInvalidUD(errors, type)
        self.finalizeErrors(table, errors)

    # работа с ошибками
    def autocorr(self, type:str, value:str):
        value    = strF.autocorrCell(type, value)       # выполнится только для нужных type
        if type == 'region':
            # сперва в autocorr без изменений, и, если не будет найдено, ещё раз после изменений
            AC = lib.autocorr.get(type,value)
            if AC['fixed']: return AC['value']
            #else:           value = STR_autocorrCity(value)   ДОПИСАТЬ
        return lib.autocorr.get(type,value)['value']    # выполнится только для нужных type
    def validate_andCapitalize(self, type:str, value:str, extra=None):
        # в extra можно передать любые необходимые доп. данные
        params = G.AStypes[type]
        # ↓ передаём в extra suggList из appUI.suggInvalidUD()
        if extra is None and params['readLib']: extra = lib.getValidationList(type)
        final  = {'valid':None, 'value':value}

        if params['checkList']:
            found          = listF.searchStr(extra, value, 'item', True, not self.justVerify)
            final['valid'] = bool(len(found))
            if not self.justVerify and final['valid']: final['value'] = found[0]
        else: final['valid'] = strF.validateCell(type, final['value'])
        return final
    def suggInvalidUD(self, errors:dict, type:str):
        # errors = {'initValue'.lower():ErrorObj,...}
        counter = {'cur':0, 'total':len(errors.keys())}
        for key,errObj in errors.items():
            counter['cur'] += 1
            suggList        = self.getSugg(type, key)

            resp = self.app.suggInvalidUD(type, errObj.initVal, suggList, counter)
            print(resp)

    def getSugg(self, type:str, value:str):
        suggList = strF.getSugg(type, value)
        return suggList
    def finalizeErrors(self, table:list, errors:dict):
        # table=[[Cell,...],...]; errors={'initValue'.lower():ErrorObj,...}
        for err in errors.values():
            for pos in err.pos:
                if err.fixed: table[pos['r']][pos['c']].value =     err.newVal
                table              [pos['r']][pos['c']].error = not err.fixed

    # чтение данных из таблицы
    def getData(self, book):
        self.file     = Excel(book, self.fullRange)
        self.file.table.cutUp(self.searchTitleRow(self.file.table.data))
        self.log .add('readFile', {'table':self.file.table.data, 'range':self.fullRange})

        if self.toTD:
            self.unkTD = TableDict(self.file.table)
            self.init_curTD()
        else: self.table = CellTable(self.file.table.data)
    def searchTitleRow(self, table:list):   # table – таблица[[]]
        for r in range(len(table)):
            if strF.findSubList(table[r][0], ('Уникальных: ', 'Ошибок: '), 'index') != 0: return r
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
class LEtemplate(): # общие функции для Log() и Errors()
    def __init__(self, UI, type='log'): # здесь UI = FRlog/FRerrors (фреймы)
        self.UI   = UI
        self.file = G.files[type]
        write_toFile([], self.file)
        self.initStorage()
class Log(LEtemplate):
    def initStorage(self): self.log = []
    def add(self, type:str, params=None):
        # в params можно передать любые объекты, необходимые для получения доп. данных
        new = self.getType(type, params)
        self.log  .append (new)
        write_toFile      (new, self.file, True)
        self.UI.add       (new)
    def getType(self, type:str, params=None):
        if   type == 'launch'  : final = '[core] ' + S.layout['actions'][params]['log']
        elif type == 'readFile':
            final = S.log[type]['full' if params['range'] else 'range']
            rows  = len(params ['table']) - 1*(params['range']) # считаем без заголовка
            cols  = len(params ['table'][0])
            final = final.replace('%1', str(cols)+' '+strF.getEnding_forCount(S.words_byCount['столбцы'], cols))
            final = final.replace('%2', str(rows)+' '+strF.getEnding_forCount(S.words_byCount['строки' ], rows))
        return final
class ErrorLog(LEtemplate):
    def initStorage(self): self.storage = {}    # {type:{initLow:string,...},...}
    def add(self, errors:dict, type:str):
        # errors = {'initValue'.lower():ErrorObj,...}
        if type not in self.storage.keys(): self.storage[type] = {}
        for low,err in errors.items():
            newEntry = '['+type+'] ['+str(len(err.pos))+' шт.] ' + err.initVal

            self.storage[type][low] = newEntry
            write_toFile(newEntry, self.file, True)
            self.UI.add (type, low, newEntry)
class Errors():
    def __init__(self, UI):
        self.storage = {}   # {type:{initLow:ErrorObj,...},...}
        self.log     = ErrorLog(UI,'errors')
    def add(self, errors:dict, type:str):
        # errors = {'initValue'.lower():ErrorObj,...}
        if type not in self.storage.keys(): self.storage[type] = {}
        self.storage[type] .update(errors)
        self.log.add(errors, type)
    def suggest(self):
        pass

class ErrorObj():
    def __init__(self, initValue:str, row:int, col:int):
        self.initVal = initValue
        self.newVal  = None
        self.fixed   = False
        self.pos     = [{'r':row, 'c':col}] # список всех позиций этой ошибки в диапазоне проверки [{'r':row, 'c':col},...]
    def addPos(self, row:int, col:int):
        self.pos.append({'r':row, 'c':col})

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
