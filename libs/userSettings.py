# можно использовать в других программах
from   sys import exit as SYSEXIT
import globalFuncs     as GF

class userCfg():
  def __init__(self,file :str):
    def _init():
      self.storage = GF.get_initSettings()  # self.storage – основное хранилище всех настроек
      self.write()

    self.file = file
    try   : self.read()
    except:     _init()
  def get     (self,param:str):
    # для упрощения кода в param педедаём section:key с разделителем
    section,key = param.split(':')
    try:    return self.storage[section][key]
    except: return True
  def set     (self,param:str,value,saveFile=True):
    # для упрощения кода в param педедаём section:key с разделителем
    section,key = param.split(':')
    if section not in self.storage.keys(): self.storage[section] = {}
    self.storage[section][key] = value
    if saveFile: self.write()
  def read    (self):
    def _toStorage(list:list):
      def _setType():
        match type:
          case 'bool': return val == 'True'
          case 'int' : return int(val)
          case  _    : return     val

      self.storage = {}
      for line in list:
        key,type,val = line.split(' ',2)
        self.set(key,_setType(),False)
    _toStorage    (GF.readFile(self.file))
  def write   (self):
    def _parse():
      final = []
      for section,paramDict in self.storage.items():
        for   key,value     in paramDict   .items():
          final.append(section+':'+key     +' '+  # ключ
                       type(value).__name__+' '+  # тип данных
                       str (value))               # значение
      return final
    GF.write_toFile(_parse(),self.file)

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
