from   sys import exit as SYSEXIT
from   copy        import deepcopy
import xlwings         as xw
import globalVars      as G
from   excelRW     import Excel
import libReading      as libR
import stringFuncs     as strF
import listFuncs       as listF

# общие функции
def getValidationList(type:str):
    if type == 'title': return columns.vList

# шаблоны классов
class AStemplate(): # autocorr & sugg
    def __init__(self,table,vList=False):   # table = объект tables.Table()
        # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
        self.data = libR.parseAS(table.data,vList)
    def get(self,type:str,value:str):
        if type in self.data.keys(): return listF.searchStr(tuple(self.data[type].keys()),value)
        else:                        return []

# классы библиотек
class Columns():
    def __init__(self,table):   # table = объект tables.Table()
        # vList = validation list, список допустимых значений
        self.data  = libR.parseDoubleDict(table.data)
        self.vList = [params['title'] for params in self.data.values()]
    def getKey_byTitle(self,title:str,fullText=False,lower=False,stripTitle=False):
        # возвращает, например, ключ 'region' по заголовку 'Регион и город'
        for key,params in self.data.items():
            if strF.findSub(params['title'],title,'bool',fullText,lower,('','b')[stripTitle]): return key
class Autocorr(AStemplate):
    def get(self,type:str,value:str):
        keys = super().get(type,value)
        if len(keys): return {'fixed':True, 'value':self.data[type][keys[0]]}
        else:         return {'fixed':False,'value':value}
class Sugg(AStemplate):
    pass
class Regions():
    def __init__(self,table):   # table = объект tables.Table()
        self.data = libR.parseRegions(table.data)
        self.initLists()
    def initLists(self):
        self.  vList = []                       # validation list, список допустимых значений
        self.regList = deepcopy(G.initRegList)  # список всех регионов
        for list in self.data.values():
            for item in list:
                self.vList.append(item['id'])   # все ID, в т. ч. дублей по названию
                if not item['region'] in self.regList: self.regList.append(item['region'])
            if len(list) == 1: self.vList.append(list[0]['city'])   # только если  не дубли  по названию

# создаём библиотеки, аналог глобальных переменных
try:
        with xw.App(visible=False) as app:
            book = xw.Book(G.files['lib'])
            raw  = Excel(book,'shAll',('toStrings'))
            book.close()    # иначе, если других окон Excel не открыто, останется пустое окно
        columns  = Columns (raw.data['columns'] ['table'])
        autocorr = Autocorr(raw.data['autocorr']['table'],False)
        sugg     = Sugg    (raw.data['sugg']    ['table'],True)
        regions  = Regions (raw.data['regions'] ['table'])
        del raw # удаляем из памяти
        ready    = True
except: ready    = False

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
