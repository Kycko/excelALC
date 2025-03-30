from   sys import exit as SYSEXIT
from   copy        import deepcopy
import xlwings         as xw
import globalsMain     as G
from   excelRW     import Excel
import libReading      as libR

# шаблоны классов
class AStemplate    (): # autocorr & sugg
    def __init__(self,table,vList=False):   # table = объект tables.Table()
        # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
        self.data = libR.parseAS(table.data,vList)
class RegCatTemplate(): pass

# классы библиотек
class Columns ():
    def __init__(self,table):   # table = объект tables.Table()
        # vList = validation list, список допустимых значений
        self.data  = libR.parseDoubleDict(table.data)
        self.vList = [params['title'] for params in self.data.values()]
class Autocorr(AStemplate): pass
class Sugg    (AStemplate): pass
class Regions (RegCatTemplate):
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
