from   sys         import exit as SYSEXIT
from   globalFuncs import curDateTime,write_toFile
import globalsMain     as G
import strings         as S
import appUI
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
    def _initLE():  # LE = log & errors
      self.log =   Log(self.UI)
      self.log.add    ('mainLaunch',{'time':curDateTime(),'file':book['file']})
      # self.log.add    ('launchType',  type)
      # self.errors = Errors(self.UI.errors,self.log,initStr)

    self.pr   =  G.dict.tasks[type]
    self.type =  type
    self.cfg  = {param:G.config.get(type+':'+param) for param in self.pr['cfg']}
    _initLE()

# журнал и ошибки
class Log():  # журнал
  def __init__(self,UI:appUI.Window):
    self.UI   = UI
    self.files = {'main'   :G.files[  'mLog'],
                  'changes':G.files[ 'chLog'],
                  'errors' :G.files['errLog']}
    for file in self.files.values(): write_toFile([],file)
  def add(self,type:str,rpl:dict=None):
    # rpl=replace (словарь строк для замены переменных)
    def _write  ():
      write_toFile(newStr,self.files[file],True)
      self.UI.log (newStr,unit,file)
    def _getType():
      unit  =  G.dict.log ['units'][type]
      final = '['+unit+'] ' + S.log[type]
      for key,val in rpl.items(): final = final.replace('$'+key+'$',val)
      return final,unit
    newStr,unit = _getType()
    for file in G.dict.log['files'][unit]: _write()

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
