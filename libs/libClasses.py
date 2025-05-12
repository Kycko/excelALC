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
    case 'region'   : return regions.vList
    case 'ACregions': return regions.vListAC
    case 'cat'      : return cat    . cat_vList
    case 'vert'     : return cat    .vert_vList
    case 'source'   : return sources.data

# шаблоны классов
class     AStemplate(): # autocorr & sugg
  def __init__(self,table,vList=False): # table = объект tables.Table()
    # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
    self.data = libR.parseAS(table.data,vList)
  def get(self,type:str,value:str,fullText:bool):
    # fullText = True для autocorr, False для sugg
    if type in self.data.keys():
      keys = strF.findSubList(value,tuple(self.data[type].keys()),'item',True,fullText)
      return [self.data[type][key] for key in keys]
    else: return []
class RegCatTemplate():
  def parseMain(self,table,cols:tuple,cKey:str,pKey:str):
    # table = объект tables.Table(); cKey,pKey = core key, parent key
    core_vList,pList,self.doubles = [],[],[]  # pList = parents list
    self.core,self.parent         = cKey,pKey

    self.data  = libR.parseDict(table.data,cols)
    for low,list in self.data.items():
      for   item in list:
        core_vList.append(item['id']) # все ID, в т. ч. дублей
        val = item[pKey]
        if pKey == 'region':  val = val.lower()
        if not val in pList:  pList.append(val)
      if len(list) == 1: core_vList.append(list[0][cKey]) # только не дубли по названию
      else:            self.doubles.append(low)
    return core_vList,pList
  def getDoubleSuggs(self,value:str):
    final = []
    found = strF.findSubList(value.lower(),self.doubles,'item',True,False,False)
    for low in found:
      for u in self.data[low]:  # u = unique
        final.append({'val':u['id'],
                      'btn':u['id']+' ['+u[self.core]+', '+u[self.parent]+']'})
    return final

# классы библиотек
class Autocorr(AStemplate):
  def get    (self,type:str,value:str):
    res   = super().get(type,value,True)
    return {'fixed': bool(res),
            'value': res [0]['val'] if bool(res) else value}
  def getSugg(self,type:str,value:str): return super().get(type,value,False)
class Sugg    (AStemplate):
  def get(self,type:str,value:str):
    final,res = [],super().get(type,value,False)
    if res:
      for list in res: final += list
    if type in ('cat','region') and len(value) > 2:
      # ↑ чтобы для 1-2 букв не выдавало огромный список
      lib    = cat if type == 'cat' else regions
      final += lib.getDoubleSuggs(value)
      final += autocorr  .getSugg(type,value)
    return self.rmDoubles(final)
  def rmDoubles(self,list:list):
    final,addedValues = [],[] # addedValues = значения, которые мы добавили в final
    for dict in list:
      value = dict['val'].lower()
      if value not in addedValues:
        addedValues.append(value)
        final      .append(dict)
    return final
class Cat     (RegCatTemplate):
  def __init__(self,table): # table = объект tables.Table()
    self.cat_vList,self.vert_vList = super().parseMain(table,(0,3,4),'cat','vert')
class Regions (RegCatTemplate):
  def __init__(self,cities,regVars,AClib:dict): # cities и regVars = объекты tables.Table()
    def _parseVars():
      for row in regVars.data[1:]:
        fromLow = row[0].lower()
        self.regVars.append(fromLow)
        AClib[fromLow] = libR.get_ACto(row[1])
      self.regVars.sort(key=len,reverse=True) # сортирует от длинных к коротким
    self.vList,self.regVars = super().parseMain(cities,(0,1,2),'city','region')
    self.vListAC = self.vList + list(AClib.keys()) # для функции strF.RCtry()
    _parseVars()
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
  sugg        = Sugg         (raw.data['sugg']      ['table'],True)
  regions     = Regions      (raw.data['regions']   ['table'],
                              raw.data['regionVars']['table'],
                              autocorr.data['region'])
  cat         = Cat          (raw.data['cat']       ['table'])
  sources     = oneCol_toList(raw.data['sources']   ['table'])
  del raw # удаляем из памяти
  ready       = True
except: ready = False

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
