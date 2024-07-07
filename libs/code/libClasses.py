from   sys import exit as SYSEXIT
import libReading      as libR
import stringFuncs     as strF

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

# создаём библиотеки, аналог глобальных переменных
try:
        raw     = libR.readFile()
        columns = Columns(raw['columns'])
        ready   = True
except: ready   = False

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
