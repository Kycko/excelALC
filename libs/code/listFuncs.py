from   sys import exit as SYSEXIT
import stringFuncs     as strF

def searchStr(list:list, txt:str, type='item', fullText=True, lower=True, getFirst=True):
    # type может быть 'item' (вернёт подходящие элементы списка) или 'index' (вернёт индексы)
    # getFirst=True возвращает только первый найденный
    final = []
    for i in range(len(list)):
        if strF.findSub(list[i], txt, 'bool', fullText, lower):
            if type == 'item': found = list[i]
            else             : found = i
            if getFirst      : return found
            else             : final.append(found)
    if getFirst: return None
    else:        return final

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
