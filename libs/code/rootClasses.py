from   sys import exit as SYSEXIT
from   os          import startfile
from   globalFuncs import curDateTime,write_toFile
import globalVars      as G
import appUI
from   excelRW     import Excel
from   tables      import CellTable,Table,TableDict
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
        self.stages     = None  # всегда сбрасываем для правильной работы allChecks

        params          = G.launchTypes[type]
        self.type       = type
        self.log        = Log(self.UI)
        self.readRange  = params['readRange']
        self.toTD       = params['toTD']    # будем работать с TableDict (True) или же с CellTable (False)
        self.addHeader  = params['addHeader']
        self.justVerify = params['justVerify']
        self.resetBg    = params['resetBg']
        self.hlTitles   = params['hlTitles']

        self.uCfg       = {param: G.config.get(type+':'+param) for param in params['getUserCfg']}
        self.uCfg  .update(params['forceUserCfg'])

        self.initLE (book.name) # LE = log & errors
        self.getData(book,TDrmRC=params['TDrmRC'])  # получаем данные

        if   params['launch'] == 'allChecks' : self.launchRangeChecker('title')
        elif params['launch'] == 'reCalc'    : self.fullTDchecker()
        elif params['launch'] == 'capitalize': self.capitalizationLaunched()
        elif params['launch'] == 'rmEmptyRC' :
            self.rmEmptyRC(self.table)
            self.finish   ()
        elif params['launch'] == 'checkVert' :
            if self.file.data[self.shName]['range'].columns.count != 1: self.UI.launchErr('oneColumn')
            else:
                cats = self.updData_forVertChecker()
                if cats is None: self.UI.launchErr('noCatsColumn')
                else:
                    self.vertChecker(self.table.data,cats.data)
                    self.finish()
        elif params['launch'] == 'fillBlanks': self.fillBlanks()
        else                                 : self.launchRangeChecker(params['AStype'])
    def launchRangeChecker(self,type:str):
        if type == 'title': data = [[column.title for column in self.unkTD.columns.values()]]
        else:               data =     self.table.data
        self.rangeChecker(data,type)
    def   nextStage       (self):
        # запускает проверку следующего столбца для 'allChecks'
        columns = self.curTD.columns
        if self.stages is None: self.stages = list(columns.keys())
        if self.stages:
            curCol = columns[self.stages.pop(0)]
            temp   = curCol.type.split(':')
            type   = temp.pop(0)
            if len(temp): self.subtype = temp[0]

            if     type  == 'vert':
                if 'cat' in   columns.keys(): self. vertChecker([curCol.cells],[columns['cat'].cells])
            elif   type  in G.AStypes.keys(): self.rangeChecker([curCol.cells], type)
            else                            : self. nextStage  ()
        else: self.finish()

    def initLE(self,bookName:str):  # LE = log & errors
        initStr = S.log['mainLaunch'].replace('$$1',curDateTime()).replace('$$2',bookName)
        self.log.add   ('mainLaunch',initStr)
        self.log.add   ('launchType',self.type)
        self.errors = Errors(self.UI.errors,self.log,initStr)

    # основные алгоритмы проверки
    def fullTDchecker(self):
        columns = self.curTD.columns
        for col in columns.values():
            temp = col.type.split(':')
            type = temp.pop(0)
            if len(temp): self.subtype = temp[0]

            if   type == 'vert':
                if 'cat' in columns.keys(): self.vertChecker ([col.cells],[columns['cat'].cells])
            elif type in  G.AStypes.keys(): self.rangeChecker([col.cells], type)

            self.finalizeErrors()
        self.finish()
    def rangeChecker (self, table:list, type:str):
        # в table передаём либо CellTable().data, либо [cells[]] из TableColumn
        # т. е. table – это всегда [[Cell,...],...]
        self.rTable = table # range table, понадобится в self.finalizeErrors()
        errors      = {}    # {initLow:ErrorObj,...}
        for     r in range(len(table)):
            for c in range(len(table[r])):
                cell   = table[r][c]
                errPos = {'r':r,'c':c}
 
                low = cell.value.lower()
                if low in errors.keys(): errors[low].addPos(errPos)
                else:
                    tempVal = cell.value
                    VAL     = self.validate_andCapitalize(type,tempVal)
                    if not VAL['valid'] and not self.justVerify:
                        tempVal = self.autocorr(type,tempVal)
                        VAL     = self.validate_andCapitalize(type,tempVal)

                    if VAL['valid']:
                        if VAL['value'] != cell.value:
                            # ↑ если они равны, ничего делать не надо (ошибки нет)
                            errors[low] = ErrorObj(type,
                                                   cell.value,
                                                   errPos,
                                                   not self.justVerify,
                                                   (VAL['value'],None)[self.justVerify])
                            if not self.justVerify: # это только про autocorr?
                                self.log.add('ACsuccess',
                                            {'type':type,'from':cell.value,'to':VAL['value']})
                                cell.value = VAL['value']
                    else: errors[low] = ErrorObj(type,cell.value,errPos)

        self.errors.addCur(errors,type)
        self     .nextSugg()
    def  vertChecker (self,tVerts:list,tCats:list):
        # в tVerts/tCats передаём либо CellTable().data, либо [cells[]] из TableColumn: это всегда [[Cell,...],...]
        AClogger     = []       # запоминаем autocorr'ы для журнала   (например, Services -> Услуги)
        errors       = {}       # {initLow:ErrorObj,...}
        vertsChanged = False    # чтобы показать сообщение про changed только один раз

        for     r in range(len(tVerts)):
            for c in range(len(tVerts[r])):
                VC     = tVerts[r][c]               # это vert cell (CellObj)
                lowCat = tCats [r][c].value.lower() # это string
                CVstr  = tCats[r][c].value+' | '+VC.value   # 'cat | vert'
                errPos = {'r':r,'c':c}
                CVlib  = lib.cat.catVertList        # cat & vert
                new    = CVlib[lowCat] if lowCat in CVlib.keys() else ''

                CVlow  = CVstr.lower()
                if  CVlow in errors.keys():
                    errors[CVlow].addPos(errPos)
                    fRow       = errors[CVlow].pos[0]['r']
                    fCol       = errors[CVlow].pos[0]['c']
                    VC.value   = tVerts[fRow][fCol].value
                    VC.error   = tVerts[fRow][fCol].error
                    VC.changed = tVerts[fRow][fCol].changed
                else:
                    if self.justVerify or not self.uCfg['autocorr']:
                        if new != VC.value:
                            errors[CVlow] = ErrorObj('vert',CVstr,errPos)
                            VC.error      = True
                    else:
                        ACval = self.autocorr('vert',VC.value)
                        if new:
                            if VC   .value   != new: self.logVert(AClogger,CVstr,new)
                            if ACval.lower() != new.lower():
                                if VC.value:
                                    errors[CVlow] = ErrorObj('vert',CVstr,errPos,True,new)
                                    VC.changed    = True
                                    vertsChanged  = True
                        else:
                            errors[CVlow] = ErrorObj('vert',CVstr,errPos)
                            VC.error = True
                        VC.value = new

        if vertsChanged: self.log.add('vertChanged')
        self.errors.addCur(errors,'vert')
        if self.type == 'allChecks': self.nextStage()
    def rmEmptyRC    (self,tObj):
        # tObj = CellTable либо TableDict
        self.log.add('RCremoved',tObj.rmEmptyRC('rc',self.uCfg['rmTitled']))
    def capitalizationLaunched(self):
        type = self.uCfg['selected']
        for     row  in self.table.data:
            for cell in row:
                new = strF.capitalize(cell.value,type)
                if new != cell.value:
                    self.log.add('ACsuccess',{'type':type,'from':cell.value,'to':new})
                cell.value = new
        self.finish()
    def fillBlanks   (self):
        filler = self.uCfg['filler']
        count  = 0
        for     row  in self.table.data:
            for cell in row:
                if not cell.value:
                    cell.value = filler
                    count     += 1

        self.log.add('blanksFilled',count)
        self. finish()

    # работа с ошибками
    def autocorr(self,type:str,value:str):
        initVal  = value
        value    = strF.autocorrCell(type,value,self.uCfg)  # выполнится не для всех type (кроме strip())
        if type == 'region':
            # сперва в autocorr без изменений, и, если не будет найдено, ещё раз после изменений
            AC = lib.autocorr.get(type,value)
            if AC['fixed']: return AC['value']
            else:  value = strF.ACcity(value,lib.regions.parentList,lib.get_vList('ACregions'))
        AC = lib.autocorr.get(type,value)   # выполнится не для всех type
        if type == 'region' and not listF.inclStr(lib.regions.vList,AC['value']):
            return lib.regions.ACregionID(initVal)
        else: return AC['value']
    def validate_andCapitalize(self,type:str,value:str,extra=None):
        # в extra можно передать любые необходимые доп. данные
        params = G.AStypes[type]
        # ↓ передаём в extra suggList из appUI.suggInvalidUD()
        if extra is None and params['readLib']: extra = lib.get_vList(type)
        final  = {'type'  :type,
                  'value' :value,
                  'valid' :None,
                  'errKey':''}  # ключ сообщения для suggUI

        if params['checkList']:
            found          = listF.searchStr(extra,value,'item',True,not self.justVerify)
            final['valid'] = bool(found)
            if final['valid']:
                if not self.justVerify: final['value'] = found[0]
            else: final['errKey'] = 'notInList'
        else:
            if type == 'phone' and self.type in ('allChecks','reCalc'): self.uCfg['noBlanks'] = False
            strF.validateCell(final,self.uCfg)   # final обновляется внутри этой функции
        return final
    def getSuggList(self,errObj):
        type,value = errObj.type,errObj.initVal
        if G.AStypes[type]['getLibSugg']: return lib .sugg   .get(type,value)
        else:                             return strF.getSuggList(type,value)
    def nextSugg(self):
        queue = self.errors.suggQueue
        if queue and not self.justVerify and G.AStypes[queue[0].type]['showSugg'] and self.uCfg['suggestErrors']:
            suggList = self.getSuggList(queue[0])
            self.UI      .suggInvalidUD(queue[0],suggList,len(queue))
        else:
            if not self.justVerify      : self.UI.setSuggState(False)
            if     self.type != 'reCalc': self.finalizeErrors (self.type == 'allChecks')
    def suggFinalClicked(self,OKclicked:bool,newValue=''):
        self.errors.suggClicked(OKclicked,newValue)
        self.nextSugg()
    def finalizeErrors(self,forceTitles=False):
        for  errObj in self.errors.curData.values():
            for i in range(len(errObj.pos)):
                # self.rTable – это всегда [[Cell,...],...]
                errPos = errObj .pos[i]
                cell   = self.rTable[errPos['r']][errPos['c']]
                if errObj.type == 'title' and i: cell.error = True
                else:
                    cell.error = not errObj.fixed
                    if errObj.fixed: cell.value = errObj.newVal

        if             self.readRange ==   'selection': self.table.data = self.rTable
        elif forceTitles or self.type == 'checkTitles': self.TDfinalizeTitles()
        if                  self.type ==   'allChecks': self.nextStage()
        elif                self.type !=    'reCalc'  : self.finish()
    def TDfinalizeTitles(self):
        # сперва переносим исправленные
        keys = []   # ключи[(unkKey,curKey),...], которые потом надо будет переместить из unkTD в curTD
        for unkKey,column in self.unkTD.columns.items():
            if not column.title.error:
                keys.append((unkKey,lib.columns.getKey_byTitle(column.title.value)))
        for item in keys: self.move_fromUnkTD_toCurTD(item[0],item[1])

        # затем добавляем обязательные
        rows = len(tuple(self.curTD.columns.values())[0].cells)
        for key,params in lib.columns.data.items():
            if params['mandatory'] and key not in self.curTD.columns.keys():
                self.curTD.addEmptyColumn(key,params['title'],rows,lib.columns.data[key]['type'])
                self.log  .add ('columnAdded',params['title'])
    def logVert(self,AClogger:list,prev:str,new:str):
        if prev not in AClogger:
            AClogger.append(prev)
            self.log.add   ('ACsuccess',
                            {'type':'vert','from':prev,'to':new})

    # чтение данных из таблицы
    def getData(self,book,logging=True,TDrmRC=False):
        # book – это сам объект книги из xlwings; TDrmRC – сразу удаляем пустые столбцы/строки
        self.file = Excel(book,self.readRange,('toStrings'))

        # for выполнится один раз; обращение через .keys()[0] и .values()[0] не работает
        for shName,tObj in self.file.data.items():
            self.shName = shName
            if self.readRange == 'shActive': tObj['table'].cutUp(self.searchTitleRow(tObj['table'].data))
            if logging:
                self.log.add('readSheet',shName)
                self.log.add('readFile',
                            {'tObj':tObj,'range':('range','full')[self.readRange == 'shActive']})

            if self.toTD:
                self.unkTD = TableDict(tObj['table'])
                if TDrmRC: self.rmEmptyRC(self.unkTD)
                self.init_curTD()
            else: self.table = CellTable(tObj['table'])
    def updData_forVertChecker(self):
        # возвращает Table из тех же строк столбца с заголовком 'Категория' + обновляет self.file по selection'у
        catIndex           = self.searchTitleCol(lib.columns.data['cat']['title'])
        if  len(catIndex) == 1:
            range          = self.file.data[self.shName]['range']
            cats           = self.file.getValues(range.offset(0,catIndex[0]+1-range.column))
            self.readRange = 'selection'
            self.getData(self.file.file,False)
            return CellTable(Table(cats,('toStrings')))
    def searchTitleRow(self,table:list):    # table = таблица[[]]
        for r in range(len(table)):
            if strF.findSubList(table[r][0],('Уникальных: ','Ошибок: '),'index') != 0: return r
        return 0
    def searchTitleCol(self,title:str):
        # возвращает индексЫ (список[]) столбцов с заголовком title, отсекая шапку (errors/unique)
        rawTable = self.file.data[self.shName]['table'].data
        titleRow = rawTable      [self.searchTitleRow(rawTable)]
        return listF.searchStr(titleRow,title,'index',True,False)
    def init_curTD(self):
        self.curTD = TableDict()
        for libKey,params in lib.columns.data.items():
            unkKey = self.unkTD.searchTitle(params['title'])
            if unkKey is not None:
                self.unkTD.columns[unkKey].title.value = params['title']    # для правильной капитализации
                self.move_fromUnkTD_toCurTD(unkKey,libKey)
    def move_fromUnkTD_toCurTD(self,unkKey:str,curKey:str):
        self.curTD.columns[curKey] = self.unkTD.columns.pop(unkKey)
        check = curKey in lib.columns.data.keys()
        self.curTD.columns[curKey].type = lib.columns.data[curKey]['type'] if check else None

    # финальные шаги (преобразование и запись)
    def finish (self):
        count = self.errors.getCount()
        if self.toTD:
            self.joinTDs()
            self.curTD_toTable()
        self.finalWrite   ()
        self.finalColors  (count['errors'])
        if G.config   .get(self.type + ':saveAfter'):
            self.file.save()
            self.log .add ('fileSaved')
        self.UI    .finish(count['errors'])
    def joinTDs(self):  # объединяем curTD и unkTD перед финальной записью
        for key in tuple(self.unkTD.columns.keys()): self.move_fromUnkTD_toCurTD(key,key)
    def curTD_toTable(self):
        if 'reorder' in self.uCfg .keys() and self.uCfg['reorder']: self.finalTDreorder()
        self.table    = self.curTD.toCellTable(self.addHeader,lib.columns.data,S.tblHeader)
    def finalTDreorder(self):
        # изменяет в столбцах свойство initPos, по которому они будут расставлены при записи
        keys    = list(self.curTD.columns.keys())
        counter = 0

        # сперва из библиотеки
        for key in lib.columns.data.keys():
            if key in keys:
                keys.remove(key)
                self.curTD.columns[key].initPos = counter
                counter += 1

        # затем с неправильными названиями
        for i in sorted([int(key) for key in keys]):
            self.curTD.columns[str(i)].initPos = counter
            counter += 1

        self.log.add('titlesReordered')
    def finalWrite(self):
        newSheet  = G  .config.get(self.type + ':newSheet')
        self.tObj = self.table.toTable()
        equal     = self.tObj.equals(self.file.data[self.shName]['table'])
        if not equal:
            self.file.data [self.shName]['table'] = self.tObj
            self.file.write(self.shName,self.readRange,newSheet)
        self.log.add('finalWrite',{'sheet':newSheet,'equal':equal})
    def finalColors(self,totalErrors:int):
        self.file.resetBgColors(self.shName,self.resetBg)
        self.log .add        ('colorErrors',totalErrors)

        # шапку подсвечиваем в любом случае
        last = len(self.table.data) if totalErrors in range(1,501) else (0,2)[self.addHeader]
        for row in range(last): self.hlRow(row,'errors')

        if self.hlTitles: self.hlRow(self.searchTitleRow(self.tObj.data),'goodTitles')
        if self.type in ('launchAll','checkVert'):
            for row in range(len(self.table.data)): self.hlRow(row,'chVerts')   # changed verticals
    def hlRow(self,r:int,type:str):
        # r,c = row,column; type может быть 'errors' или 'goodTitles'
        for c in range(len(self.table.data[r])):
            err        =   self.table.data[r][c].error
            chg        =   self.table.data[r][c].changed
            if   type == 'errors'     and     err: self.setCellColor(r,c,'hlError')
            elif type == 'chVerts'    and     chg: self.setCellColor(r,c,'hlChanged')
            elif type == 'goodTitles' and not err: self.setCellColor(r,c,'goodTitle')
    def setCellColor(self,row:int,col:int,colorKey:str):
        self.file.setCellColor(self.readRange,self.shName,row,col,G.colors[colorKey])

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
        if   type == 'mainLaunch'     : final = params
        elif type == 'launchType'     : final = S.layout['actions'][params]['log']
        elif type == 'readSheet'      : final = S.log[type].replace('$$1',params)
        elif type == 'readFile'       :
            final = S.log[type][params['range']]
            rows  = len(params['tObj']['table'].data) - 1*(params['range'] == 'full') # считаем без заголовка
            cols  = len(params['tObj']['table'].data[0])
            final = final.replace('$$1',params['tObj']['addr'])
            final = final.replace('$$2',str(cols)+' '+strF.getEnding_forCount(S.words_byCount['столбцы'],cols))
            final = final.replace('$$3',str(rows)+' '+strF.getEnding_forCount(S.words_byCount['строки' ],rows))
        elif type == 'ACsuccess'      :
            final = S.log[type].replace('$$1',params['type'])
            final = final      .replace('$$2',params['from'])
            final = final      .replace('$$3',params['to'])
        elif type == 'errorsFound'    :
            final = S.log[type].replace('$$1',params['type']).replace('$$2',str(params['count']))
        elif type == 'suggFinished'   :
            # здесь params = ErrorObj()
            final = tuple(S.log[type].values())[params.fixed].replace('$$1',params.type)
            final =                                     final.replace('$$2',params.initVal)
            if params.fixed: final =                    final.replace('$$3',params.newVal)
        elif type == 'titlesReordered': final = S.log[type]
        elif type == 'columnAdded'    : final = S.log[type].replace('$$1',params)
        elif type == 'RCremoved'      :
            r,c   = len(params['rows']),len(params['cols'])
            final = S.log[type][('none','main')[bool(r or c)]].replace('$$1',str(r)).replace('$$2',str(c))
        elif type == 'vertChanged'    : final = S.log[type]
        elif type == 'blanksFilled'   : final = S.log[type].replace('$$1',str(params))
        elif type == 'finalWrite'     :
            key    = 'skip' if params['equal'] else 'main'
            final  =      S.log[type][key]
            if key == 'main': final = final.replace('$$1',S.log[type]['sheet'][params['sheet']])
        elif type == 'colorErrors'    :
            if    not params: key = '0'
            elif params > 99: key = 'skip'
            else            : key = 'done'
            final = S.log[type][key].replace('$$1',str(params))
        elif type == 'fileSaved'      : final = S.log[type]

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
        self.curData = errors
        self.getSuggQueue()
        if errors:
            self.add_mData(errors,type)
            self.log()
    def rmFixed(self,errObj):
        # удаляем из фрейма в UI и из файла, оставляем в self.curData со статусом fixed
        self.UI  .rm(errObj)
        self.updFile()

    # вспомогательные
    def add_mData(self,errors:dict,type:str):   # errors = {initLow:ErrorObj,...}
        if type in self.mData.keys():
            for low,errObj in errors.items():
                if low in self.mData[type].keys():
                    errObj.updFrom_mData(self.mData[type][low])
                    self.mData[type][low].pos += errObj.pos
                else: self.mData[type][low]    = errObj
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
    def updFile(self):  # перезаписывает файл, проверяя весь self.mData
        final = [self.initLogStr]
        for typeErrors in self.mData.values():
            for errObj in typeErrors.values():
                if not errObj.fixed: final.append(self.getLogEntry(errObj))
        write_toFile(final,self.file)
    def getCount(self):
        final = {'errors':0,'total':0}
        for typeErrors in self.mData.values():
            for errObj in typeErrors.values():
                count = len(errObj.pos)
                final['total']                       += count
                if not errObj.fixed: final['errors'] += count
        return final

    # журналы
    def log(self):
        for errObj in self.suggQueue:
            newEntry = self.getLogEntry(errObj)
            write_toFile(newEntry,self.file,True)
            self.UI .add(errObj.type,errObj.initVal.lower(),newEntry)
        if self.suggQueue:
            self.mainLog.add('errorsFound',{'type':errObj.type,'count':len(self.suggQueue)})
    def getLogEntry(self,errObj):
        return '['+errObj.type+'] ['+str(len(errObj.pos))+' шт.] ' + errObj.initVal
    def showNotepad(self): startfile(self.file)
class ErrorObj():   # объект одной ошибки, используется в хранилище Errors()
    def __init__(self,type:str,initValue:str,pos:dict,initFixed=False,newVal=None):
        # pos={'r':row,'c':col}
        self.type    = type # тип ошибки, один из G.AStypes
        self.initVal = initValue
        self. newVal =  newVal
        self.fixed   = initFixed
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
