from   sys         import exit as SYSEXIT
from   globalFuncs import curDateTime,write_toFile
import globalsMain     as G
import appUI
from   excelRW     import Excel
from   tables      import Table,CellTable
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

    self.pr   =  G.dict.tasks[type]
    self.type =  type
    self.cfg  = {param:G.config.get(type+':'+param) for param in self.pr['cfg']}
    _initLE ()
    _getData(rmRC=self.pr['rmRC_onRead'])

  # чтение данных из таблицы
  def searchTitleRow(self,table:Table):
    for r in range(len(table.data)):
      if strF.findSubList(table[r][0],('Уникальных: ','Ошибок: '),'index') != 0: return r
    return 0

# журнал и ошибки
class Log():    # журнал
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
class Errors(): # хранилище ошибок
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

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
