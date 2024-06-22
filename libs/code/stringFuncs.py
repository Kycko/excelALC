from sys         import exit as SYSEXIT
from globalFuncs import getIB

# получение правильного окончания в зависимости от количества
def getEnding_forCount(words:dict, count:int):
    # примеры words есть в words_byCount (модуль strings)
    ten   = count % 10  # остаток деления
    hundr = count % 100 # остаток деления
    if   ten == 0 or ten > 4 or hundr in (11, 12, 13): return words['many']
    elif ten == 1:                                     return words['1']
    else:                                              return words['2-4']

# поиск
def findSubList(string:str, list:list, type='index', fullText=False, lower=True):
    # ищет в строке каждый элемент списка; type может быть 'index', 'bool' и 'item'
    # индекс – это позиция найденного в string, 'item' вернёт найденный элемент списка list
    for item in list:
        result = findSub(string, item, 'index', fullText, lower)
        if result >= 0: return item if type == 'item' else getIB(type, result)
    return None if type == 'item' else getIB(type, -1)
def findSub(string:str, sub:str, type='index', fullText=False, lower=True):
    # type может быть 'index' или 'bool'
    # если fullText=True, проверяется равенство строк (но после .trim() + можно задать lower=True)
    # если lower   =True, все строки будут сравниваться через .toLowerCase()
    string = string.strip()
    sub    = sub   .strip()

    if fullText and len(string) != len(sub): return getIB(type, -1)
    if lower:
        string = string.lower()
        sub    = sub   .lower()

    return getIB(type, string.find(sub))

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
