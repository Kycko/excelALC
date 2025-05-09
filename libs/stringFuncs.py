from sys         import exit as SYSEXIT
from globalFuncs import getIB

# получение правильного окончания в зависимости от количества
def ending_byCount(count:int):
  ten   = count % 10  # остаток деления
  hundr = count % 100 # остаток деления
  if   ten == 0 or ten > 4 or hundr in range(11,15): return 'many'
  elif ten == 1:                                     return '1'
  else:                                              return '2-4'

# поиск (общие)
def findSubList(string:str,list:list,type='item',multi=False,fullText=False,lower=True,strip=''):
  # ищет в строке каждый элемент списка list[] и возвращает их индекс(ы) или item('ы)
  # type = 'index' (позиция найденного в string) или 'item' (вернёт найденные элементы списка list)
  # multi: вернуть все найденные или только первое найденное
  final = []
  for item in list:
    result = findSub(string,item,'index',fullText,lower,strip)
    if result >= 0:
      new = item if type == 'item' else result
      if multi: final.append(new)
      else    : return       new
  return final if multi else (None,-1)[type == 'index']
def findSub(string:str,sub:str,type='index',fullText=False,lower=True,strip=''):
  # type может быть 'index' или 'bool'
  # если fullText=True, проверяется равенство строк (но после .trim() + можно задать lower=True)
  # если lower   =True, все строки будут сравниваться через .toLowerCase()
  # strip может быть '', 'a' (для string), 'b' (для sub), 'ab'
  if 'a' in strip: string = string.strip()
  if 'b' in strip: sub    = sub   .strip()

  if fullText and len(string) != len(sub): return getIB(type,-1)
  if lower:
    string = string.lower()
    sub    = sub   .lower()

  return getIB(type,string.find(sub))

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
