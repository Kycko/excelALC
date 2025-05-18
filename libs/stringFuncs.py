from   sys         import exit as SYSEXIT
from   globalFuncs import getIB
import globalsMain     as G
import listFuncs       as listF

# получение правильного окончания в зависимости от количества
def ending_byCount(count:int):
  ten   = count % 10  # остаток деления
  hundr = count % 100 # остаток деления
  if   ten == 0 or ten > 4 or hundr in range(11,15): return 'many'
  elif ten == 1:                                     return '1'
  else:                                              return '2-4'

# проверка и исправление разных пользовательских данных (общие)
def autocorrCell(type:str,value:str,params=None):
  def _autocorrPMW(value):  # phone,mail,website
    RPL = {'from':('​','\n','﻿','–','—','|',';',',,'),  # RPL=replace
           'to'  :('',',' ,''  ,'-','-',',',',',',')}
    for i in range(len(RPL['from'])): value = value.replace(RPL['from'][i],RPL['to'][i])

    list = value.lower().split(',')
    for i in range(len(list)):
      item = list[i].strip()
      match type:
        case 'phone':
          item = ''.join(c for c in item if c.isdigit())  # удаляем всё, кроме цифр
          if len(item) in (10,11): item = '7'+item[-10:]  # после этого проверить badPhone
          if len(item)  <  10 or item == G.dict.badPhone: item = ''
        case 'mail':
          parts = item.split('@')
          if 'gmail' in parts[-1]: parts[-1] = 'gmail.com'
          parts = '@'.join(parts).split('.')
          if   parts[-1] in ('r','u') : parts[-1] = 'ru'
          elif parts[-1] in ('c','co'): parts[-1] = 'com'
          item = '.'.join(parts)
        case 'website':
          item = rmStartList(item,G.dict.badWebStarts,0,False).rstrip('/')
          if  checkStartList(item,G.dict.rmSites,'bool',False): item = ''
          else:
            item = cut_ifFound(item,'?ysclid='       ,'end',False)      # трекинг Яндекса
            item = cut_ifFound(item,'?yclid='        ,'end',False)      # трекинг Яндекса
            item = cut_ifFound(item,'?utm_campaign=' ,'end',False)
            item = cut_ifFound(item,'?utm_medium=  ' ,'end',False)
            item = cut_ifFound(item,'?utm_referrer=' ,'end',False)
            item = cut_ifFound(item,'?utm_source='   ,'end',False)
            item = cut_ifFound(item,'?roistat='      ,'end',False)
            item = cut_ifFound(item,'hh.ru/','start',False,'',True,13)  # напр., '[perm.]hh.ru/...
      list[i] = item  # для удобства именования внутри используем item

    list     =  listF.rmDoublesStr(listF.rmBlankStr(list))
    if type == 'phone' and not list and params['noBlanks']: return G.dict.badPhone
    return ','.join(list)

  value = value.strip()
  if   type ==  'cat':
    return ' '.join(strips(value,G.dict.strips[type]).split())
  elif type in ('phone','mail','website'): return _autocorrPMW(value)
  else:                                    return  value
def validateCell(vObj:dict,params=None):  # vObj={'type':,'value':,'valid':,'errKey':}
  def _checkPMW(type:str,value:str):  # PMW = phone,mail,website
    # возвращаем valid:True/False и ключ для S.errInput[type]
    match type:
      case 'phone':
        pnb = params['noBlanks']
        if not pnb and value    == ''             : return True,''
        if not pnb and value    == G.dict.badPhone: return False,'secNines'
        if         len(value)   != 11             : return False,'length'
        if             value[0] != '7'            : return False,'firstSymb'
        if             value[1] in '67'           : return False,'kazakh'
      case 'mail':
        if value            == ''             : return True ,''
        if value.count('@') != 1              : return False,'dogCount'
        if inclSubList(value,G.dict.ruSymbols): return False,'ru'
        if '$'      in value                  : return False,'$'

        name,dom = value.split('@')
        end      = dom  .split('.')[-1]
        if  not '.' in dom: return False, 'dotDomain'
        if     '..' in dom: return False,'dotsDomain'
        if len(end) ==  1 : return False, 'endDomain'
        if     end == 'co': return False, 'endCo'
        if    name  in       G.dict.allHyphens: return False,'hyphen'
        if inclSubList(value,G.dict.badSymbols[type],False,False):
          return False,'badSymbols'
      case 'website':
        if value      ==    '': return True ,''
        if not    '.' in value: return False,'dot'
        if value.endswith('/'): return False,'endSlash'
        if checkStartList(value,G.dict.badWebStarts,'bool'): return False,'wwwHttp'
        if checkStartList(value,G.dict.rmSites     ,'bool'): return False,'rmSites'
        if    inclSubList(value,G.dict.badSymbols[type],False,False):
          return False,'badSymbols'
        if findSub       (value,'?ysclid='    ,'bool'): return False,'yaTrack'

        index = findSub(value,'hh.ru/')
        if index > 0: return False,'hhCity'
    return True,''
  def _validateDate(date:str):
    if not date: return True
    else:
      parts = date.split('.')
      if len(parts) == 3:
        try:
          for i in range(len(parts)): parts[i] = int(parts[i])
        except: return False

        d,m,y = parts
        if not y in range(2000,2100)              : return False
        if not m in range(1   ,13)                : return False
        if not d in range(1,G.dict.monthDays[m]+1): return False
        return True

  if   vObj['type'] in ('phone','mail','website'):
    list = vObj['value'].split(',')
    if listF.inclDoublesStr(list,True):
      vObj['valid'],vObj['errKey'] = False,'listDoubles'
      return
    if vObj['type'] == 'phone' and len(list) > 1 and G.dict.badPhone in list:
      vObj['valid'],vObj['errKey'] = False,'nines_inMany'
      return
    for item in list:
      vObj['valid'],vObj['errKey'] = _checkPMW(vObj['type'],item)
      if not        vObj['valid']: return
    if vObj['type'] in ('mail','website'): vObj['value'] = vObj['value'].lower()
  elif vObj['type'] == 'date':
    vObj['valid'] = _validateDate(vObj['value'])
    if not vObj['valid']:
      vObj['errKey'] = 'format'
      return
  vObj['valid'] = True
def  getSuggList(type:str ,value:str):
  final = []
  if type in ('mail','website'):
    new = value.replace(' ','').replace('|',',').lower()
    if new != value:
      vObj = {'type':type,'value':new,'valid':None,'errKey':''}
      validateCell(vObj)
      if vObj['valid']: final.append({'val':new,'btn':new})
  elif type ==  'date':
    parts = trySplitDate(value.strip('00:00:00').strip())
    if parts:
      for    i in range(3):
        for  j in range(3):
          if i != j:
            new = parts[i]+'.'+parts[j]+'.'+parts[3-i-j]
            if validateDate(new): final.append({'val':new,'btn':new})
  return final
def trySplitDate(date:str):
  for symb in G.dict.dateSplitters:
    parts = date.split(symb)
    if len(parts) == 3: return parts
def validateDate(date:str):
  if not date: return True
  else:
    parts = date.split('.')
    if len(parts) == 3:
      try:
        for i in range(len(parts)): parts[i] = int(parts[i])
      except: return False

      d,m,y = parts
      y = y in range(2000,2100)
      m = m in range(1,13)
      d = d in range(1,G.dict.monthDays[m]+1)
      if y and m and d: return True
  return False

# исправление регионов/городов; RC = region/city
# НАДО БУДЕТ ПЕРЕПИСАТЬ + ДОБАВИТЬ ПРОВЕРКУ РЕЗУЛЬТАТА ПОСЛЕ КАЖДОЙ ФУНКЦИИ
def ACcity(city:str,regions:list,ACregions:list):
  # ошибка при импорте lib сюда, поэтому передаём аргументами regions и ACregions
  def _fixOblast():
    list = city.split()
    for i in range(len(list)):
      if mRCtrims(list[i]).lower() in ('обл','оюл','облость'):
        list[i] = 'область'
        return ' '.join(list)
    return city
  def _rmOblast ():
    new = RCsplitRegion(city,regions)[0]
    new = _trimCity(new)  # только для проверки ACregions, приходится дублировать следующий шаг
    if new and listF.inclStr(ACregions,new): return new
    else:                                    return city
  def _trimCity (str:str):
    # сначала те, что с пробелом
    list = str.split()
    for i in (0,-1):
      list[i] = list[i].replace('(','').replace(')','')
      if listF.inclStr(G.dict.cTrims['spaced'],list[i]):
        list.pop(i)
        return ' '.join(list)

    # потом           те, что могут быть в начале строки без пробела, но в скобках
    # и сразу за ними те, что могут быть в начале строки без пробела и без скобок
    temp     = rmStartList(str,G.cTrims['start'],1)
    if temp != str: return temp

    return str
  def _try      ():
    # пробует заменять 'е'<->'ё' (в обе стороны), все пробелы на дефисы (напр., для 'Ростов на Дону')
    # и подчёркивания на пробелы/дефисы (напр., для 'Санкт_Петербург')
    # возвращает новый вариант, если получится правильный город либо подходящий под автозамену
    RPL   = {'е':'ё','ё':'е'} # RPL=replacement
    vars  = [city,
             city.replace(' ','-'),
             city.replace('_','-'),
             city.replace('_',' ')]
    vars  =  listF.rmDoublesStr                    (vars)
    found =  listF.searchAny_from_strList(ACregions,vars)
    if found is not None: return found

    for var in vars:
      for i in range(len(var)):
        if var[i] in RPL.keys():
          new = replaceIndex(var,i,RPL[var[i]])
          if   listF.inclStr(ACregions,new): return new
    return city

  city = joinSpaces(city)
  city = _fixOblast()
  city = _rmOblast ()
  city = _trimCity (city)
  city =  mRCtrims (city)
  if listF.inclStr (ACregions,city): return city

  city = lat_toCyr      (city)
  city = trimOverHyphens(city)
  city = _try()
  return city
def RCsplitRegion(string:str,regList:list):
  # ищет в string каждый регион и, если найдёт его, возвращает отдельно город и регион
  init   = string
  region = findSubList(string,regList)
  if region is not None and len(region) != len(string):
    string = mRCtrims(string.lower().replace(region.lower(),''))
    if not string: string = init
  return string,region
def mRCtrims     (city  :str):  # main region/city trims
  city = rmStartList(city,    G.dict.mrcTrims,0,False)
  while  city and city[-1] in G.dict.mrcTrims: city = city[:-1]
  return city

# поиск (общие)
def inclSubList(string:str,list:list,fullText=False,lower=True,strip=''):
  # возвращает True, если хотя бы один элемент list[] будет найден в string
  for item in list:
    if findSub(string,item,'bool',fullText,lower,strip): return True
  return False
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
def findSub    (string:str,sub :str ,type='index',fullText=False,lower=True,strip=''):
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
def checkStartList(string:str,list:list,type='item',lower=True,stripList=False):
  # проверяет каждый элемент list[]: если он в начале строки, возвращает найденное или True/False
  # type может быть 'item' или 'bool'
  for item in list:
    if findSub(string,item,'index',False,lower,('','b')[stripList]) == 0:
      return string[:len(item)] if type == 'item' else True
  return (False,None)[type == 'item']

# изменение (общие)
def strips     (string:str,symbols:tuple):
  for s in symbols: string = string.strip(s)
  return string
def cut_ifFound(string:str,sub :str ,side='end',lower=True,strip='',inclSub=False,maxCut=0):
  # ищет sub в string, обрезает начало (side='start') или конец (side='end')
  # inclSub: оставить sub в возвращаемом результате (True) или нет (False)
  # если обрежется больше, чем maxCut, то ничего не делает: вернёт изначальную string
  # maxCut=0 отключает ограничение
  index     = findSub(string,sub,'index',False,lower,strip)
  if index >= 0:
    new = string[:index] if side == 'end' else string[len(sub)+index:]
    if inclSub: new = new + sub if side == 'end' else sub + new
  else: return string

  if not maxCut or len(string)-len(new) <= maxCut: return new
  else:                                            return string
def rmStartList(string:str,list:list,count=0,lower=True,stripList=False):
  # проверяет каждый элемент списка list[]: если он в начале строки, удаляет его из начала строки
  # count = сколько раз удалять; если count=0, удаляем все, пока в начале не будет что-то другое
  iter = 0  # итерация: увеличивается на 1, когда производим удаление
  while count == 0 or (count >= 0 and iter < count):
    found = checkStartList(string,list,'item',lower,stripList)
    if not found: return string
    else:
      string = string.replace(found,'',1)
      iter  += 1
  return string
def joinSpaces (string:str):  # объединяет все мультипробелы в одинарные
  # while быстрее, чем regex и split+join
  string = string.replace(' ',' ')  # заменяем неразрывные пробелы
  while '  ' in string: string = string.replace('  ',' ')
  return string
def lat_toCyr  (string:str,allowLower=True):
  if  allowLower: string = string.lower()
  for init,to in G.dict.lat_toCyr.items():
    if not allowLower: string = string.replace(init,to)
    string = string.replace(init.lower(),to.lower())
  return string
def trimOverHyphens(string:str):
  # делит строку по дефисам, делает trim() каждой части и собирает строку обратно
  list = fixHyphens(string).split('-')
  for i in range(len(list)): list[i] = list[i].strip()
  return    '-'.join(list)
def      fixHyphens(string:str): return string.replace('—','-').replace('–','-')
def replaceIndex   (string:str,index:int,newChar:str):
    return string[:index] + newChar + string[index+1:]
def replaceVars(string:str,vars:dict):  # заменяет в string'е все $var$ на значения из vars{}
  for key,val in vars.items():
    if type(val) == str:  # защита от TypeError
      string = string.replace('$'+key+'$',val)
  return string

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
