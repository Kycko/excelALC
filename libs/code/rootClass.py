from   sys import exit as SYSEXIT
from   appUI       import Window
from   globalFuncs import write_toFile
import globalVars      as G
import strings         as S
import stringFuncs     as strF

# корневой класс: из него запускаются UI и код других модулей
class Root():
    def __init__(self):
        self.UI = Window(self)
        self.UI.mainloop()

    # основные функции
    def launch(self,book,type:str):
        # book – это сам объект книги из xlwings; type = например, 'checkEmails'
        params = G.launchTypes[type]

        # запоминаем базовые переменные
        self.type       = type
        self.log        = Log(self.UI)
        self.log.add   ('launch',type)
        #self.errors     = Errors(errors)
        #self.fullRange  = params['fullRange']
        #self.toTD       = params['toTD'] # будем работать с TableDict (true) или же с CellTable (false)
        #self.justVerify = params['justVerify']
        #if params['getSuggParam']: self.suggErrors = G.config.get(type + ':suggestErrors')

        #self.getData(book)  # получаем данные
        #if params['launch'] == 'rangeChecker': self.rangeChecker(self.table.data, params['AStype']) # проверяем выделенный диапазон

# журнал и ошибки
class Log():
    def __init__(self,UI:Window):
        self.UI   = UI
        self.file = G.files['log']
        write_toFile([],self.file)
    def add(self,type:str,params=None):
        # в params можно передать любые объекты, необходимые для получения доп. данных
        new  = self.getType(type,params)
        write_toFile(new,self.file,True)
        self.UI.log (new)
    def getType(self,type:str,params=None):
        if   type == 'launch'   : final = '[core] ' + S.layout['actions'][params]['log']
        elif type == 'readSheet': final = S.log[type].replace('$$1',params)
        elif type == 'readFile':
            final = S.log[type]['full' if params['range'] else 'range']
            rows  = len(params ['table']) - 1*(params['range']) # считаем без заголовка
            cols  = len(params ['table'][0])
            final = final.replace('$$1',params['addr'])
            final = final.replace('$$2',str(cols)+' '+strF.getEnding_forCount(S.words_byCount['столбцы'],cols))
            final = final.replace('$$3',str(rows)+' '+strF.getEnding_forCount(S.words_byCount['строки' ],rows))
        elif type == 'ACsuccess':
            final = S.log[type].replace('$$1',params['type'])
            final = final      .replace('$$2',params['from'])
            final = final      .replace('$$3',params['to'])
        elif type == 'errorsFound':
            final = S.log[type].replace('$$1',params['type']).replace('$$2',str(params['count']))
        return final

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
