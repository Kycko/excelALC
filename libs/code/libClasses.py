from   sys import exit as SYSEXIT
import libData         as D
import listFuncs       as listF
import stringFuncs     as  strF
# во всех библиотеках основное хранилище – self.data{}

# общие функции
def readDictTable(keys:list, values:dict):  # например, для чтения libColumns
    final = {}
    for column, params in values.items():
        final[column] = {}
        for i in range(len(keys)): final[column][keys[i]] = params[i]
    return final
def getValidationList(type:str):
    if type == 'title': return columns.vList

# шаблоны классов
class AStemplate(): # autocorr & sugg
    def __init__(self, libData:dict):
        self.data = libData

# классы
class libColumns():
    def __init__(self):
        self.data  = readDictTable(D.colKeys, D.colValues)
        self.vList = [params['title'] for params in self.data.values()] # vList = validation list, список допустимых значений
    def getKey_byTitle(self, title:str, fullText=False, lower=False):   # возвращает, например, ключ 'region' по заголовку 'Регион и город'
        for key, params in self.data.items():
            if strF.findSub(params['title'], title, 'bool', fullText, lower): return key
class libAutocorr(AStemplate):
    def get(self, type:str, value:str):
        if type in self.data.keys():
            keys = listF.searchStr(self.data[type].keys(), value)
            if len(keys): return {'fixed':True,  'value':self.data[type][keys[0]]}
        return                   {'fixed':False, 'value':value}
class libSugg(AStemplate):
    pass

# аналог глобальных переменных для чтения всех библиотек
columns  = libColumns ()
autocorr = libAutocorr(D.autocorr)
sugg     = libSugg    (D.sugg)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
