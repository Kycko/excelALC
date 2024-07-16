from   sys import exit as SYSEXIT
from   globalFuncs import write_toFile
import globalVars      as G
import appUI
from   excelRW     import Excel
from   tables      import CellTable,TableDict
import strings         as S
import stringFuncs     as strF
import listFuncs       as listF
import libClasses      as lib

# корневой класс: из него запускаются UI и код других модулей
class Root():
    def __init__(self):
        if lib.ready:
            self.UI = appUI.Window(self)
            self.UI.mainloop()
        else: appUI.cantReadLib()
    def launch(self,book,type:str):
        # book – это сам объект книги из xlwings; type = например, 'checkEmails'
        params = G.launchTypes[type]

        # запоминаем базовые переменные
        self.type       = type
        self.errors     = Errors(self.UI.errors)
        self.log        = Log   (self.UI)
        self.log.add('launch',type)
        self.readRange  = params['readRange']
        self.toTD       = params['toTD'] # будем работать с TableDict (True) или же с CellTable (False)
        self.justVerify = params['justVerify']
        if params['getSuggParam']: self.suggErrors = G.config.get(type + ':suggestErrors')

        self.getData(book)  # получаем данные
        if params['launch'] == 'rangeChecker': self.rangeChecker(self.table.data,params['AStype'])  # проверяем выделенный диапазон

    # основные алгоритмы проверки
    def rangeChecker(self,table:list,type:str):
        # в table передаём либо CellTable().data, либо [cells[]] из TableColumn
        # т. е. table – это всегда [[Cell,...],...]
        errors = {} # {initLow:ErrorObj,...}
        for r in range(len(table)):
            for c in range(len(table[r])):
                cell    = table[r][c]
                tempVal = cell.value
                if not self.justVerify: tempVal = self.autocorr(type,tempVal)

                VAL = self.validate_andCapitalize(type,tempVal)
                if VAL['valid']:
                    if not self.justVerify and tempVal != cell.value:
                        self.log.add('ACsuccess',{'type':type,'from':cell.value,'to':tempVal})
                        cell.value = VAL['value']
                else:
                    low = cell.value.lower()
                    if low in errors.keys (): errors[low]  .addPos             ({'r':r,'c':c})
                    else:                     errors[low] = ErrorObj(cell.value,{'r':r,'c':c})
        if errors:
            self.errors.add(errors,type,self.log)
            if self.suggErrors: self.nextSugg(type)

    # работа с ошибками
    def autocorr(self,type:str,value:str):
        value    = strF.autocorrCell(type,value)    # выполнится только для нужных type
        if type == 'region':
            # сперва в autocorr без изменений, и, если не будет найдено, ещё раз после изменений
            AC = lib.autocorr.get(type,value)
            if AC['fixed']: return AC['value']
            #else:           value = STR_autocorrCity(value)   ДОПИСАТЬ
        return lib.autocorr.get(type,value)['value']    # выполнится только для нужных type
    def validate_andCapitalize(self,type:str,value:str,extra=None):
        # в extra можно передать любые необходимые доп. данные
        params = G.AStypes[type]
        # ↓ передаём в extra suggList из appUI.suggInvalidUD()
        if extra is None and params['readLib']: extra = lib.getValidationList(type)
        final  = {'valid':None, 'value':value}

        if params['checkList']:
            found          = listF.searchStr(extra,value,'item',True,not self.justVerify)
            final['valid'] = bool(len(found))
            if not self.justVerify and final['valid']: final['value'] = found[0]
        else: final['valid'] = strF.validateCell(type, final['value'])
        return final
    def nextSugg(self,type:str):
        queue = self.errors.suggQueue
        if queue:
            suggList = self.getSugg(type,queue[0].initVal)
            self.UI  .suggInvalidUD(type,queue[0].initVal,suggList,len(queue))
    def getSugg(self,type:str,value:str):
        suggList = strF.getSugg(type,value)
        return suggList

    # чтение данных из таблицы
    def getData(self,book): # book – это сам объект книги из xlwings
        self.file = Excel(book,self.readRange)

        # for выполнится один раз; обращение через .keys()[0] и .values()[0] не работает
        for shName,tObj in self.file.data.items():
            tObj['table'].cutUp(self.searchTitleRow(tObj['table'].data))
            self.log .add('readSheet',shName)
            self.log .add('readFile' ,{'tObj' :tObj,
                                       'range':('range','full')[self.readRange == 'shActive']})

            if self.toTD:
                self.unkTD = TableDict(tObj['table'])
                self.init_curTD()
            else: self.table = CellTable(tObj['table'])
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
class Log():        # журнал
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
            final =   S.log[type][params['range']]
            rows  =           len(params['tObj']['table'].data) - 1*(params['range'] == 'full') # считаем без заголовка
            cols  =           len(params['tObj']['table'].data[0])
            final = final.replace('$$1',params['tObj']['addr'])
            final = final.replace('$$2',str(cols)+' '+strF.getEnding_forCount(S.words_byCount['столбцы'],cols))
            final = final.replace('$$3',str(rows)+' '+strF.getEnding_forCount(S.words_byCount['строки' ],rows))
        elif type == 'ACsuccess':
            final = S.log[type].replace('$$1',params['type'])
            final = final      .replace('$$2',params['from'])
            final = final      .replace('$$3',params['to'])
        elif type == 'errorsFound':
            final = S.log[type].replace('$$1',params['type']).replace('$$2',str(params['count']))
        return final
class Errors():     # хранилище ошибок
    def __init__(self,UI):
        self.storage = {}   # {type:{initLow:ErrorObj,...},...}
        self.UI      = UI   # UI = класс appUI.Errors()
        self.file    = G.files['errors']
        write_toFile([],self.file)
    def add(self,errors:dict,type:str,mainLog:Log): # errors = {initLow:ErrorObj,...}
        if type not in self.storage.keys(): self.storage[type] = {}
        self.storage[type] .update(errors)
        self.suggQueue = list(errors.values())  # очередь предложений для исправления; после проверки элемент удаляется
        for low,err   in errors.items():
            newEntry   = '['+type+'] ['+str(len(err.pos))+' шт.] ' + err.initVal
            write_toFile(newEntry,self.file,True)
            self.UI .add(type,low,newEntry)
        mainLog.add('errorsFound',{'type':type,'count':len(errors.keys())})
class ErrorObj():   # объект одной ошибки, используется в хранилище Errors()
    def __init__(self,initValue:str,pos:dict):  # pos={'r':row,'c':col}
        self.initVal = initValue
        self.newVal  = None
        self.fixed   = False
        self.checked = False    # устанавливается True, когда пользователь введёт что-то новое или нажмёт "Отмена"
        self.pos     = [pos]    # список всех позиций этой ошибки в диапазоне проверки [{'r':row,'c':col},...]
    def addPos(self,pos:dict): self.pos.append(pos)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
