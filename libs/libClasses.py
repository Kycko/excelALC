from   sys import exit as SYSEXIT
from   copy        import deepcopy
import xlwings         as xw
import globalsMain     as G
from   excelRW     import Excel
import libReading      as libR

# общие функции
def get_vList(type:str):
  match type:
    case 'title'    : return columns.vList
    case 'region'   : return regions.vList
    case 'ACregions': return regions.vListAC
    case 'cat'      : return cat    .vList
    case 'vert'     : return cat    .parentList
    case 'source'   : return sources.data

# шаблоны классов
class AStemplate    (): # autocorr & sugg
  def __init__(self,table,vList=False): # table = объект tables.Table()
    # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
    self.data = libR.parseAS(table.data,vList)
class RegCatTemplate():
  def initLists(self,core:str,parent:str):
    self.vList      = []      # validation list, список допустимых значений
    self.doubles    = []      # список core (low) с дублирующимися названиями
    self.parentList = []      # список основных регионов/ВЕРТИКАЛЕЙ
    self.core       = core    # core   = ключ основных элементов
    self.parent     = parent  # parent = ключ родительских элементов

    for low,list in self.data.items():
      for   item in list:
        self.vList.append(item['id']) # все ID, в т. ч. дублей по названию
        if not item[parent] in self.parentList: self.parentList.append(item[parent])
      if len(list) == 1: self.vList  .append(list[0][core]) # только если не дубли по названию
      else:              self.doubles.append(low)

    self.parentList.sort(key=len,reverse=True)  # сорт. длинные → короткие (важно для autocorr регионов)

# классы библиотек
class Columns ():
  def __init__(self,table): # table = объект tables.Table()
    # vList = validation list, список допустимых значений
    self.data  = libR.parseDoubleDict(table.data)
    self.vList = [params['title'] for params in self.data.values()]
class Autocorr(AStemplate): pass
class Sugg    (AStemplate): pass
class Cat     (RegCatTemplate):
  def __init__ (self,table):  # table = объект tables.Table()
    self.data = libR.parseDict(table.data,(0,3,4))
    self.initLists()
  def initLists(self):
    super().initLists('cat','vert')
    self   .catVertList = {}
    for    list in self.data.values():
      for  item in list: self.catVertList[item   ['id']]          = item   ['vert']
      if len(list) == 1: self.catVertList[list[0]['cat'].lower()] = list[0]['vert']
  # def getVerts(self,cat:str):
  #    try   : return self.data[cat.lower()]
  #    except: 
class Regions (RegCatTemplate):
  def __init__(self,table,ACvars:list):
    # table = объект tables.Table(); ACvars = ключи из autocorr regions для функции strF.RCtry()
    self.data = libR.parseDict(table.data,(0,1,2))
    self.initLists('city','region')
    self.vListAC = self.vList + ACvars
class oneCol_toList():  # один столбец записываем в список, можно использовать для разных библиотек
  def __init__(self,table,add=[]):  # table = объект tables.Table(); add = что добавить к списку
    self.data = libR.oneCol_toList(table) + add

# создаём библиотеки, аналог глобальных переменных
try:
  with xw.App(visible=False) as app:
    book      = xw.Book(G.files['lib'])
    raw       = Excel  (book,'shAll',('toStrings'))
    book.close()  # иначе, если других окон Excel не открыто, останется пустое окно
  columns     = Columns      (raw.data['columns']   ['table'])
  autocorr    = Autocorr     (raw.data['autocorr']  ['table'],False)
  sugg        = Sugg         (raw.data['sugg']      ['table'],True)
  regions     = Regions      (raw.data['regions']   ['table'],list(autocorr.data['region'].keys()))
  cat         = Cat          (raw.data['cat']       ['table'])
  regionVars  = oneCol_toList(raw.data['regionVars']['table'],regions.parentList)
  sources     = oneCol_toList(raw.data['sources']   ['table'])
  del raw # удаляем из памяти
  ready       = True
except: ready = False

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
