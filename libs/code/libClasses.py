from   sys import exit as SYSEXIT
import libReading      as libR
import stringFuncs     as strF
import listFuncs       as listF

# шаблоны классов
class AStemplate(): # autocorr & sugg
    def __init__(self,table:list,vList=False):  # table = таблица[[]]
        # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
        self.data = libR.parseAS(table,vList)
    def get(self,type:str,value:str):
        if type in self.data.keys(): return listF.searchStr(self.data[type].keys(),value)
        else:                        return []

# классы библиотек
class Columns():
    def __init__(self,table:list):  # table = таблица[[]]
        # vList = validation list, список допустимых значений
        self.data = libR.parseDoubleDict(table)
        self.vList = [params['title'] for params in self.data.values()]
    def getKey_byTitle(self,title:str,fullText=False,lower=False):
        # возвращает, например, ключ 'region' по заголовку 'Регион и город'
        for key,params in self.data.items():
            if strF.findSub(params['title'],title,'bool',fullText,lower): return key
class Autocorr(AStemplate):
    def get(self,type:str,value:str):
        keys = super().get(type,value)
        if len(keys): return {'fixed':True, 'value':self.data[type][keys[0]]}
        else:         return {'fixed':False,'value':value}
class Sugg(AStemplate):
    pass

# создаём библиотеки, аналог глобальных переменных
try:
        raw      = libR.readFile()
        columns  = Columns (raw['columns'])
        autocorr = Autocorr(raw['autocorr'],False)
        sugg     = Sugg    (raw['sugg']    ,True)
        ready    = True
except: ready    = False

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
