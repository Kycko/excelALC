from   sys         import exit as SYSEXIT
from   globalFuncs import write_toFile
import globalsMain     as G
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
    self.pr   =  G.dict.tasks[type]
    self.type =  type
    self.log  =  Log(self.UI)
    self.cfg  = {param:G.config.get(type+':'+param) for param in self.pr['cfg']}
    #initLE() ДАЛЕЕ ДЕЛАЕМ ЭТО

# журнал и ошибки
class Log():  # журнал
  def __init__(self,UI:appUI.Window):
    self.UI   = UI
    self.file = G.files['log']
    write_toFile([],self.file)

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
