from   sys import exit as SYSEXIT
import listFuncs       as listF

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
def parseAS        (table:list,vList=False):
    # AS = autocorr&sugg; table=таблица[[]]
    # vList: будет несколько 'to'[] (True для sugg) или только один (False для autocorr)
    final = {}
    for row in table[1:]:
        rType,rFrom = row[0],row[1].lower()
        if rType not in final.keys(): final[rType] = {}
        tCur = final[rType]

        new = {'val':row[2],'btn':row[3]}
        if vList:
            if not rFrom in tCur.keys(): tCur[rFrom] = []
            tCur  [rFrom].append(new)
        else: tCur[rFrom] = new
    return final
def parseRegions   (table:list):    # table = таблица[[]]
    final = {}
    for row in table[1:]:
        key = row[0].lower()
        new = {'city':row[0],'region':row[1],'id':row[2]}
        if key in final.keys(): final[key].append(new)
        else:                   final[key]     = [new]
    return final
def oneCol_toList  (table):         # table = объект tables.Table()
    # функция отрезает первую строку (заголовок)
    table.rotate()
    return table.data[0][1:]

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
