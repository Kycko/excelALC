from   sys import exit as SYSEXIT
from   copy        import deepcopy
import xlwings         as xw
import globalVars      as G
from   excelRW     import Excel
import libReading      as libR
import stringFuncs     as strF
import listFuncs       as listF

# общие функции
def get_vList(type:str):
    if   type == 'title'    : return columns.vList
    elif type == 'region'   : return regions.vList
    elif type == 'ACregions': return regions.vListAC
    elif type == 'cat'      : return cat    .vList
    elif type == 'vert'     : return cat    .parentList
    elif type == 'source'   : return sources.data

# шаблоны классов
class AStemplate(): # autocorr & sugg
    def __init__(self,table,vList=False):   # table = объект tables.Table()
        # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
        self.data = libR.parseAS(table.data,vList)
    def get(self,type:str,value:str,fullText:bool):
        # fullText = True для autocorr, False для sugg
        if  type in self.data.keys():
            keys = strF.findSubList(value,tuple(self.data[type].keys()),'item',True,fullText)
            return [self.data[type][key] for key in keys]
        else: return []
class RegCatTemplate():
    def initLists(self,core:str,parent:str):
        self.vList   = []       # validation list, список допустимых значений
        self.doubles = []       # список core (low) с дублирующимися названиями
        self.core    = core     # core   = ключ основных элементов
        self.parent  = parent   # parent = ключ родительских элементов

        for low,list in self.data.items():
            for item in list:
                self.vList.append(item['id'])   # все ID, в т. ч. дублей по названию
                if not item[parent] in self.parentList: self.parentList.append(item[parent])
            if len(list) == 1: self.vList  .append(list[0][core])   # только если не дубли по названию
            else:              self.doubles.append(low)

        self.parentList.sort(key=len,reverse=True)  # сортирует от длинных к коротким (важно для autocorr регионов)
    def getDoubleSuggs(self,value:str):
        final = []
        found = strF.findSubList(value.lower(),self.doubles,'item',True,False,False)
        for low in found:
            for u in self.data[low]:    # u = unique
                final.append({'val':u['id'],
                              'btn':u['id']+' ['+u[self.core]+', '+u[self.parent]+']'})
        return final
    def getID(self,core:str,parent:str):
        lCore = core  .lower()
        lPar  = parent.lower()
        if    lCore in self.data.keys():
            for var in self.data[lCore]:
                if var[self.parent].lower() == lPar: return var['id']
        return ''

# классы библиотек
class Columns():
    def __init__(self,table):   # table = объект tables.Table()
        # vList = validation list, список допустимых значений
        self.data  = libR.parseDoubleDict(table.data)
        self.vList = [params['title'] for params in self.data.values()]
    def getKey_byTitle(self,title:str,fullText=True,lower=False,strip=''):
        # возвращает, например, ключ 'region' по заголовку 'Регион и город'
        for key,params in self.data.items():
            if strF.findSub(params['title'],title,'bool',fullText,lower,strip): return key
class Autocorr(AStemplate):
    def get(self,type:str,value:str):
        res   = super().get(type,value,True)
        return {'fixed': bool(res),
                'value': res [0]['val'] if bool(res) else value}
    def getSugg(self,type:str,value:str): return super().get(type,value,False)
class Sugg(AStemplate):
    def get(self,type:str,value:str):
        final = []
        res   = super().get(type,value,False)
        if res:
            for list in res: final += list
        if type in ('cat','region') and len(value) > 2: # чтобы для 1-2 букв не выдавало огромный список
            lib    = cat if type == 'cat' else regions
            final += lib.getDoubleSuggs(value)
            final += autocorr  .getSugg(type,value)
        return self.rmDoubles(final)
    def rmDoubles(self,list:list):
        final       = []
        addedValues = []    # значения, которые мы добавили в final
        for dict in list:
            value = dict['val'].lower()
            if value not in addedValues:
                addedValues.append(value)
                final      .append(dict)
        return final
class Cat(RegCatTemplate):
    def __init__(self,table):   # table = объект tables.Table()
        self.data       = libR.parseDict(table.data,(0,3,4))
        self.parentList = []    # список всех вертикалей
        self.initLists()
    def initLists(self):
        super().initLists('cat','vert')
        self   .catVertList = {}
        for list in self.data.values():
            for  item in list: self.catVertList[item   ['id']]          = item   ['vert']
            if len(list) == 1: self.catVertList[list[0]['cat'].lower()] = list[0]['vert']
    # def getVerts(self,cat:str):
    #     try   : return self.data[cat.lower()]
    #     except: 
class Regions(RegCatTemplate):
    def __init__(self,table,ACvars:list):
        # table = объект tables.Table(); ACvars = ключи из autocorr regions для функции strF.RCtry()
        self.data = libR.parseDict(table.data,(0,1,2))
        self.parentList = deepcopy(G.initRegList)   # список всех регионов
        self.initLists('city','region')
        self.vListAC = self.vList + ACvars
    def ACregionID(self,value:str):
        # аналог autocorr'а (Autocorr().get()) для дублей по названиям
        temp        = strF.RCfixOblast  (strF.joinSpaces(value))
        city,region = strF.RCsplitRegion(temp,self.parentList)
        if region is not None: city = self.getID(city,region)
        return city if city else value
class oneCol_toList():  # один столбец записываем в список, можно использовать для разных библиотек
    def __init__(self,table):   # table = объект tables.Table()
        self.data = libR.oneCol_toList(table)

# создаём библиотеки, аналог глобальных переменных
try:
        with xw.App(visible=False) as app:
            book = xw.Book(G.files['lib'])
            raw  = Excel(book,'shAll',('toStrings'))
            book.close()    # иначе, если других окон Excel не открыто, останется пустое окно
        columns  = Columns      (raw.data['columns'] ['table'])
        autocorr = Autocorr     (raw.data['autocorr']['table'],False)
        sugg     = Sugg         (raw.data['sugg']    ['table'],True)
        regions  = Regions      (raw.data['regions'] ['table'],list(autocorr.data['region'].keys()))
        cat      = Cat          (raw.data['cat']     ['table'])
        sources  = oneCol_toList(raw.data['sources'] ['table'])
        del raw # удаляем из памяти
        ready    = True
except: ready    = False

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
