from   sys import exit as SYSEXIT
import globalVars      as G
import xlwings         as xw

# читаем справочник
def readFile():
    xw.App().visible = False
    book  = xw.Book(G.files['lib'])
    final = {}
    for sheet in book.sheets:
        final[sheet.name] = sheet.used_range.options(ndim=2).value      # ndim=2 всегда даёт двумерный массив
    book.close()
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

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
