from   sys import exit as SYSEXIT
from   copy        import deepcopy
import xlwings         as xw
import globalsMain     as G
from   excelRW     import Excel
import libReading      as libR
import stringFuncs     as strF

# общие функции
def get_vList(type:str):
  match type:
    # case 'title'    : return columns.vList
    # case 'region'   : return regions.vList
    # case 'ACregions': return regions.vListAC
    case 'cat'      : return cat    . cat_vList
    case 'vert'     : return cat    .vert_vList
    case 'source'   : return sources.data

# шаблоны классов
class AStemplate(): # autocorr & sugg
  def __init__(self,table,vList=False): # table = объект tables.Table()
    # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
    self.data = libR.parseAS(table.data,vList)
  def get(self,type:str,value:str,fullText:bool):
    # fullText = True для autocorr, False для sugg
    if type in self.data.keys():
      keys = strF.findSubList(value,tuple(self.data[type].keys()),'item',True,fullText)
      return [self.data[type][key] for key in keys]
    else: return []

# классы библиотек
class Autocorr(AStemplate):
  def get(self,type:str,value:str):
    res   = super().get(type,value,True)
    return {'fixed': bool(res),
            'value': res [0]['val'] if bool(res) else value}
  def getSugg(self,type:str,value:str): return super().get(type,value,False)
class Cat():
  def __init__(self,table): # table = объект tables.Table()
    self.data = libR.parseDict(table.data,(0,3,4))
    self.cat_vList,self.vert_vList = [],[]
    for low,list in self.data.items():
      for   item in list:
        self.cat_vList.append(item['id']) # все ID, в т. ч. дублей по названию
        if not item['vert'] in self.vert_vList: self.vert_vList.append(item['vert'])
      if len(list) == 1: self.cat_vList.append(list[0]['cat'])  # только если не дубли по названию
class oneCol_toList():  # один столбец в список, можно исп. для разных библиотек
  def __init__(self,table): # table = объект tables.Table()
    self.data = libR.oneCol_toList(table)

# создаём библиотеки, аналог глобальных переменных
try:
  with xw.App(visible=False) as app:
    book      = xw.Book(G.files['lib'])
    raw       = Excel  (book,'shAll',('toStrings'))
    book.close()  # иначе останется пустое окно, если других Excel'ей не открыто
  # columns     = Columns      (raw.data['columns']   ['table'])
  autocorr    = Autocorr     (raw.data['autocorr']  ['table'],False)
  # sugg        = Sugg         (raw.data['sugg']      ['table'],True)
  # regions     = Regions      (raw.data['regions']   ['table'],
  #                             raw.data['regionVars']['table'],
  #                             list(autocorr.data['region'].keys()))
  cat         = Cat          (raw.data['cat']       ['table'])
  sources     = oneCol_toList(raw.data['sources']   ['table'])
  del raw # удаляем из памяти
  ready       = True
except: ready = False

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
