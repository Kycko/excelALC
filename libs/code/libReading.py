from   sys import exit as SYSEXIT
import globalVars      as G
import listFuncs       as listF
import xlwings         as xw

# читаем справочник
def readFile():
    final = {}
    with xw.Book(G.files['lib']) as book:
        for sheet in book.sheets:
            final[sheet.name] = sheet.used_range.options(ndim=2,empty='').value  # ndim=2 всегда даёт двумерный массив
    return final

# преобразуем данные из справочника в словари и списки
def parseDoubleDict(table:list):    # table = таблица[[]]
    # считывает в словарь {key:{prop:value,...},...}; например, для чтения lib.columns
    final = {}
    props = table.pop(0)[1:]    # props = properties
    for row in table:
        key        = row.pop(0)
        final[key] = {}
        for i in range(len(props)):
            if row[i] in ('true','false'): value = row[i] == 'true'
            else:
                try:    value = int(row[i])
                except: value =     row[i]
            final[key][props[i]] = value
    return final
def parseAS(table:list,vList=False):
    # AS = autocorr&sugg; table=таблица[[]]
    # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
    final = {}
    for row in table[1:]:
        rType   = row.pop(0)
        rFrom   = row.pop(0).lower()    # в row остались только варианты 'to'
        if rType not in final.keys(): final[rType] = {}

        if vList:
            rTo = listF.rmBlankStr(row)
            if not len(rTo): rTo = ['']
        else: rTo = row[0]
        final[rType][rFrom] = rTo
        print(rTo)
    return final

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
