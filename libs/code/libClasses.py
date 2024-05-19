from   sys import exit as SYSEXIT
import libData         as D
import stringFuncs     as strF
# во всех библиотеках основное хранилище – self.data {}

# общие функции
def readDictTable(keys:list, values:dict):  # например, для чтения libColumns
    final = {}
    for column, params in values.items():
        final[column] = {}
        for i in range(len(keys)): final[column][keys[i]] = params[i]
    return final

# классы
class libColumns():
    def __init__(self):
        self.data = readDictTable(D.colKeys, D.colValues)
    def getKey_byTitle(self, title:str, fullText=False, lower=False):   # возвращает, например, ключ 'city' по заголовку 'Регион и город'
        for key, params in self.data.items():
            if strF.findSub(params['title'], title, 'bool', fullText, lower): return key

# аналог глобальных переменных для чтения всех библиотек
columns = libColumns()

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
