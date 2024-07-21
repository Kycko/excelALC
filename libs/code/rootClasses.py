from   sys import exit as SYSEXIT
from   globalFuncs import curDateTime,write_toFile
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
        self.log        = Log(self.UI)
        self.readRange  = params['readRange']
        self.toTD       = params['toTD'] # будем работать с TableDict (True) или же с CellTable (False)
        self.justVerify = params['justVerify']
        if params['getSuggParam']: self.suggErrors = G.config.get(type + ':suggestErrors')

        self.initLE (book.name) # LE = log & errors
        self.getData(book)  # получаем данные
        if params['launch'] == 'rangeChecker': self.rangeChecker(self.table.data,params['AStype'])  # проверяем выделенный диапазон
    def initLE(self,bookName:str):  # LE = log & errors
        initStr = S.log['mainLaunch'].replace('$$1',curDateTime()).replace('$$2',bookName)
        self.log.add   ('mainLaunch',initStr)
        self.log.add   ('launchType',self.type)
        self.errors = Errors(self.UI.errors,self.log,initStr)

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
                    if low in errors.keys (): errors[low]  .addPos                  ({'r':r,'c':c})
                    else:                     errors[low] = ErrorObj(type,cell.value,{'r':r,'c':c})
        if errors:
            self.errors.addCur    (errors,type)
            if self.suggErrors: self.nextSugg()
            else:               self.finalizeErrors()

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
        final  = {'type'  :type,
                  'value' :value,
                  'valid' :None,
                  'errKey':''}  # ключ сообщение для suggUI

        if params['checkList']:
            found          = listF.searchStr(extra,value,'item',True,not self.justVerify)
            final['valid'] = bool(len(found))
            if not self.justVerify and final['valid']: final['value'] = found[0]
        else:  strF.validateCell(final) # final обновляется внутри этой функции
        return final
    def getSuggList(self,errObj):
        suggList = strF.getSuggList(errObj.type,errObj.initVal)
        return suggList
    def nextSugg(self):
        queue    = self.errors.suggQueue
        suggList = self.getSuggList(queue[0])
        self.UI      .suggInvalidUD(queue[0],suggList,len(queue))
    def suggFinalClicked(self,OKclicked:bool,newValue=''):
        if self.errors.suggClicked(OKclicked,newValue): self.nextSugg()
        else:
            self.UI.setSuggState(False)
            self .finalizeErrors()
    def finalizeErrors(self):
        for low,errObj in self.errors.curData.items():
            print(low+' '+str(errObj.fixed)+' '+str(errObj.newVal))

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
        newStr,unit = self.getType(type,params)
        write_toFile(newStr,self.file,True)
        self.UI.log (newStr,unit)
    def getType(self,type:str,params=None):
        if   type == 'mainLaunch': final = params
        elif type == 'launchType': final = S.layout['actions'][params]['log']
        elif type == 'readSheet' : final = S.log[type].replace('$$1',params)
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
        elif type == 'suggFinished':
            # здесь params = ErrorObj()
            final = tuple(S.log[type].values())[params.fixed].replace('$$1',params.type)
            final =                                     final.replace('$$2',params.initVal)
            if params.fixed: final =                    final.replace('$$3',params.newVal)

        unit  = G.log['units'][type]
        final =    '['+unit+'] '+final
        return final,unit
class Errors():     # хранилище ошибок
    def __init__(self,UI,mainLog:Log,initLogStr:str):
        # self.  mData{type:{initLow:ErrorObj,...},...} для всех ошибок (m = main)
        # self.curData      {initLow:ErrorObj,...}      только для текущей проверки
        # (разделяем для правильной работы комплексных проверок, например, launchAll)
        self.mData      = {}
        self.UI         = UI            # UI = класс appUI.Errors()
        self.mainLog    = mainLog       # основной журнал Root().log
        self.initLogStr = initLogStr    # время запуска и имя проверяемого файла, нужно для self.updFile()
        self.file       = G.files['errors']
        self.updFile()
    def addCur(self,errors:dict,type:str):  # errors = {initLow:ErrorObj,...}
        self.add_mData(errors,type)
        self.curData = errors
        self.getSuggQueue()
        self.log()
    def rmFixed(self,errObj):   # удаляем из фрейма в UI и из файла, оставляем в self.curData со статусом fixed
        self.UI.rm(errObj)
        self.updFile()

    # вспомогательные
    def add_mData(self,errors:dict,type:str):   # errors = {initLow:ErrorObj,...}
        if type in self.mData.keys():
            for low,errObj in errors.items():
                if low in self.mData[type].keys(): errObj.updFrom_mData(self.mData[type][low])
                else:                              self.mData[type][low] = errObj
        else: self.mData[type] = errors
    def getSuggQueue(self):
        self.suggQueue = [] # очередь предложений для исправления; после проверки элемент удаляется
        for errObj in self.curData.values():
            if errObj.newVal is None: self.suggQueue.append(errObj)
    def suggClicked(self,OKclicked:bool,newValue:str):
        curError = self.suggQueue.pop(0)
        curError.suggFinished(OKclicked,newValue)
        self.mainLog.add('suggFinished',curError)
        if OKclicked: self.rmFixed(curError)    # значит, исправление принято (оно валидно)
        return self.suggQueue
    def updFile(self):  # перезаписывает файл, проверяя весь self.mData
        final = [self.initLogStr]
        for typeErrors in self.mData.values():
            for errObj in typeErrors.values():
                if not errObj.fixed: final.append(self.getLogEntry(errObj))
        write_toFile(final,self.file)

    # журналы
    def log(self):
        for errObj in self.suggQueue:
            newEntry = self.getLogEntry(errObj)
            write_toFile(newEntry,self.file,True)
            self.UI .add(errObj.type,errObj.initVal.lower(),newEntry)
        self.mainLog.add('errorsFound',{'type':errObj.type,'count':len(self.suggQueue)})
    def getLogEntry(self,errObj): return '['+errObj.type+'] ['+str(len(errObj.pos))+' шт.] ' + errObj.initVal
class ErrorObj():   # объект одной ошибки, используется в хранилище Errors()
    def __init__(self,type:str,initValue:str,pos:dict): # pos={'r':row,'c':col}
        self.type    = type # тип ошибки, один из G.AStypes
        self.initVal = initValue
        self. newVal = None
        self.fixed   = False
        self.pos     = [pos]    # список всех позиций этой ошибки в диапазоне проверки [{'r':row,'c':col},...]
    def addPos(self,pos:dict): self.pos.append(pos)
    def suggFinished(self,fixed:bool,newVal:str):
        self.fixed  = fixed
        self.newVal = newVal
    def updFrom_mData(self,errObj): self.suggFinished(errObj.fixed,errObj.newVal)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
