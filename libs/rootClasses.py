from   sys         import exit as SYSEXIT
from   globalFuncs import curDateTime,write_toFile
import globalsMain     as G
import appUI
from   excelRW     import Excel
from   tables      import Table,CellTable
import strings         as  S
import stringFuncs     as  strF
import listFuncs       as listF
import libClasses      as lib

# корневой класс: из него запускаются UI и код других модулей
class Root():
  def __init__(self):
    if lib.ready:
      self.UI = appUI.Window(self)
      self.UI.mainloop()
    else: appUI.cantReadLib()
  def launch  (self,book,type:str):
    # book = {obj:,file:,sheet:}; type = например, 'chkCat'
    def _initLE (): # LE = log & errors
      self.log = Log(self.UI)
      initStr  = self.log.add('mainLaunch',{'time':curDateTime(),'file':book['file']})
      self.log.add           ('launchType',{'str' :S.UI['tasks'][type]['log']})
      self.errors = Errors(self.log,self.UI,initStr)
    def _getData(logging=True,rmRC=False):
      def _getLog():
        rng  = ('range','full')[self.pr['read'] == 'shActive']
        type = 'readRange:'+rng

        rpl = {'addr':tObj['addr']}
        c   =     len(tObj['table'].data[0])
        r   =     len(tObj['table'].data) - 1*(rng == 'full') # без заголовка
        rpl['cols'] = str(c)+' '+S.wordEndings['столбцы'][strF.ending_byCount(c)]
        rpl['rows'] = str(r)+' '+S.wordEndings['строки' ][strF.ending_byCount(r)]
        return type,rpl
      self.file = Excel(book['obj'],self.pr['read'],('toStrings'))
      for shName,tObj in self.file.data.items():
        # for выполнится один раз; обращение через .keys()[0] и .values()[0] не работает
        self.shName = shName
        if self.pr['read'] == 'shActive':
          tObj['table'].cutUp(self.searchTitleRow(tObj['table']))
        if logging:
          self.log.add('readSheet',{'sheet':shName})  # имя листа
          self.log.add(*_getLog())                    # диапазон

        if self.pr['toTD']:
          pass
          # self.unkTD = TableDict(tObj['table'])
          # if rmRC: self.rmEmptyRC(self.unkTD)
          # self.init_curTD()
        else: self.table = CellTable(tObj['table'])
    def _runType():
      match self.pr['launch']:
        case _: self.rangeChecker(self.table.data,type)

    self.pr   =  G.dict.tasks[type]
    self.type =  type
    self.cfg  = {param:G.config.get(type+':'+param) for param in self.pr['cfg']}
    _initLE ()
    _getData(rmRC=self.pr['rmRC_onRead'])
    _runType()

  # основные алгоритмы проверки
  def rangeChecker(self,table:list,type:str):
    # в table передаём либо CellTable().data, либо [cells[]] из TableColumn
    # т. е. table – это всегда [[Cell,...],...]
    self.rTable = table # range table, понадобится в self.finalizeErrors()
    errors      = {}    # {initLow:ErrorObj,...}
    for   r in range(len(table)):
      for c in range(len(table[r])):
        cell   =   table[r][c]
        errPos = {'r':r,'c':c}

        low = cell.value.lower()
        if low in errors.keys (): errors[low].addPos(errPos)
        else:
          tempVal = cell.value
          VAL     = self.validate_andCapitalize(type,tempVal)
          if not VAL['valid'] and not self.pr['justVerify']:
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

  # работа с ошибками
  def autocorr(self,type:str,value:str):
    initVal  = value
    value    = strF.autocorrCell(type,value,self.cfg) # выполн. не для всех type (кроме strip())
    if type == 'region':
      # сперва в autocorr без изменений, и, если не будет найдено, ещё раз после них
      AC = lib.autocorr.get(type,value)
      if AC['fixed']: return AC['value']
      else:  value = strF.ACcity(value,lib.regions.parentList,lib.get_vList('ACregions')) # ИЗМ. PARENTLIST
    AC = lib.autocorr.get(type,value) # выполнится не для всех type
    if type == 'region' and not listF.inclStr(lib.regions.vList,AC['value']):
      return lib.regions.ACregionID(initVal)
    else: return AC['value']
  def validate_andCapitalize(self,type:str,value:str,extra=None):
    # в extra можно передать любые необходимые доп. данные
    params = G.dict.AStypes[type]
    # ↓ передаём в extra suggList из appUI.suggInvalidUD()
    if extra is None and params['readLib']: extra = lib.get_vList(type)
    final   = {'type'  :type,
               'value' :value,
               'valid' :None,
               'errKey':''} # ключ сообщения для suggUI

    if params['checkList']:
      found          = listF.searchStr(extra,value,'item',True,not self.pr['justVerify'])
      final['valid'] = bool(found)
      if final['valid']:
        if not self.pr['justVerify']: final['value'] = found[0]
      else: final['errKey'] = 'notInList'
    else: strF.validateCell(final,self.uCfg)  # final обновляется внутри
    return final

  # чтение данных из таблицы
  def searchTitleRow(self,table:Table):
    for r in range(len(table.data)):
      if strF.findSubList(table[r][0],('Уникальных: ','Ошибок: '),'index') != 0: return r
    return 0

# журнал и ошибки
class Log():      # журнал
  def __init__(self,UI:appUI.Window):
    self.UI   = UI
    self.file = G.files['log']
    write_toFile([],self.file)
  def add(self,type:str,rpl:dict=None):
    # rpl=replace (словарь строк для замены переменных)
    def _getType():
      unit  =  G.dict.log[type]
      final = '['+unit+'] ' + S.log[type]
      for key,val in rpl.items(): final = final.replace('$'+key+'$',val)
      return final,unit
    newStr,unit = _getType()
    write_toFile(newStr,self.file,True)
    self.UI.log (newStr,unit)
    return newStr # пока что нужно только для _initLE()
class Errors():   # хранилище ошибок
  def __init__ (self,log:Log,UI:appUI.Window,initLogStr:str):
    self.curQueue   = []  # очередь текущей проверки, в ней же будут ссылки на UI labels
    self.errorsLeft = []  # что не исправлено (нужно для подсвечивания в файле)
    self.log        = log # основной журнал Root().log
    self.UI         = UI
    self.file       = G.files['errors']
    self.write(initLogStr,False)
  # def add_noFix(self) потом доработать, это запись ошибок без исправления
  def write(self,str:str,justAdd=True):
    write_toFile   ([str],self.file,justAdd)
    self.UI.buildUI('log',self.UI.wx['rl:errors'],{'text':str})
class ErrorObj(): # объект одной ошибки, используется в хранилище Errors()
  def __init__(self,type:str,initValue:str,pos:dict,initFixed=False,newVal=None):
    # pos={'r':row,'c':col}
    self.type    =  type  # тип ошибки, один из G.AStypes
    self.initVal =  initValue
    self. newVal =   newVal
    self.fixed   =  initFixed
    self.pos     = [pos]  # список всех позиций в диапазоне проверки [{'r':,'c':},...]
  def addPos  (self,pos :dict): self.pos.append(pos)

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
