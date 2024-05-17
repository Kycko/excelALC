from sys         import exit as SYSEXIT
from globalFuncs import getIB

# поиск
def findSubList(string, list, type='index', fullText=False, lower=True):
    # ищет в строке каждый элемент списка; type может быть 'index', 'bool' и 'item'
    # индекс – это позиция найденного в string, 'item' вернёт найденный элемент списка list
    for item in list:
        result = findSub(string, item, 'index', fullText, lower)
        if result >= 0: return item if type == 'item' else getIB(type, result)
    return None if type == 'item' else getIB(type, -1)
def findSub(string, sub, type='index', fullText=False, lower=True):
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
