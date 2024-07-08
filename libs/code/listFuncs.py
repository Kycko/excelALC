from   sys import exit as SYSEXIT
import stringFuncs     as strF

# поиск
def searchStr(list:list,txt:str,type='item',fullText=True,lower=True):
    # type может быть 'item' (вернёт подходящие элементы списка) или 'index' (вернёт индексы)
    final = []
    for i in range(len(list)):
        if strF.findSub(list[i],txt,'bool',fullText,lower):
            if type == 'item': final.append(list[i])
            else             : final.append(i)
    return final
def inclStr(list:list,txt:str,fullText=True,lower=True):
    # есть ли строка среди элементов списка
    for item in list:
        if strF.findSub(item,txt,'bool',fullText,lower): return True
    return False

# изменение
def rmDoublesStr(oldList:list,lower=False):
    newList = []
    for item in oldList:
        if not inclStr(newList,item,True,lower): newList.append(item)
    return newList
def rmBlankStr(list:list):
    while '' in list: list.remove('')
    return list

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
