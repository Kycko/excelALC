from   sys import exit as SYSEXIT
import stringFuncs     as strF

# поиск
def searchStr(list:list,txt:str,type='item',fullText=True,lower=True,strip=''):
  # type может быть 'item' (вернёт подходящие элементы списка) или 'index' (вернёт индексы)
  # strip может быть '','a'(для элементов list),'b'(для txt),'ab'
  final = []
  for i in range(len(list)):
    if strF.findSub(list[i],txt,'bool',fullText,lower,strip):
      final.append (list[i] if type == 'item' else i)
  return final
def inclStr(list:list,txt:str,fullText=True,lower=True,strip=''):
  # есть ли строка среди элементов списка
  for item in list:
    if strF.findSub(item,txt,'bool',fullText,lower,strip): return True
  return False
def inclDoublesStr(oldList:list,lower=False):
  # для оптимизации не подменяем на rmDoublesStr() со сравнением длины списков
  newList = []
  for item in oldList:
    if inclStr(newList,item,True,lower): return True  # здесь оптимизация
    else:                                newList.append(item)
  return False
def searchAny_from_strList(root:list,vars:list,type='item',fullText=True,lower=True,strip=''):
  # если в первом списке есть хотя бы один элемент второго списка, вернёт index/item из первого списка
  # type может быть 'item' или 'index'
  for i in range(len(root)):
    if inclStr(vars,root[i],fullText,lower,strip): return (i,root[i])[type == 'item']
  return (-1,None)[type == 'item']

# изменение
def rmDoublesStr(oldList:list,lower=False):
  newList = []
  for item in oldList:
    if not inclStr(newList,item,True,lower): newList.append(item)
  return newList
def rmBlankStr(list:list):  # оставлю такую функцию для простоты
  while '' in list: list.remove('')
  return list

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
