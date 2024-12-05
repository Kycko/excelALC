from   sys         import exit as SYSEXIT
from   globalFuncs import getIB
import globalVars      as G
import listFuncs       as listF

# получение правильного окончания в зависимости от количества
def getEnding_forCount(words:dict,count:int):
    # примеры words есть в words_byCount (модуль strings)
    ten   = count % 10  # остаток деления
    hundr = count % 100 # остаток деления
    if   ten == 0 or ten > 4 or hundr in range(11,15): return words['many']
    elif ten == 1:                                     return words['1']
    else:                                              return words['2-4']

# проверка и исправление разных пользовательских данных (общие)
def autocorrCell(type:str,value:str,params=None):
    value = value.strip()
    if   type ==  'cat'                    :
        return ' '.join(value.strip('.').strip('-').strip('|').split())
    elif type in ('phone','mail','website'): return   AC_PMW(type,value,params)
    else:                                    return               value
def AC_PMW(type:str,value:str,params=None): # AutoCorr Phone,Mail,Website
    RPL = {'from': ('​','﻿','–','—','|',';',',,'),  # RPL = replace
           'to'  : ('',''  ,'-','-',',',',',',' )}
    for i in range(len(RPL['from'])): value = value.replace(RPL['from'][i],RPL['to'][i])

    list = value.lower().split(',')
    for i in range(len(list)):
        item = list[i].strip()  # обрезает пробелы и проч. по бокам
        if   type == 'phone':
            item = ''.join(c for c in item if c.isdigit())                  # удаляем всё, кроме цифр
            if   len(item) == 11                      : item = '7'+item[1:] # после этого проверить badPhone
            elif len(item) == 10                      : item = '7'+item     # после этого проверить badPhone
            if   len(item)  < 10 or item == G.badPhone: item = ''
        elif type == 'mail':
            parts = item.split('@')
            if 'gmail' in parts[-1]: parts[-1] = 'gmail.com'
            item = '@'.join(parts)
        elif type == 'website':
            item = rmStartList(item,G.badWebStarts,0,False).rstrip('/')
            if  checkStartList(item,G.rmSites,'bool',False): item = ''
            else:
                item = cut_ifFound(item,'?ysclid=','end',False)             # трекинг Яндекса
                item = cut_ifFound(item,'hh.ru/','start',False,'',True,13)  # напр., '[perm.]hh.ru/...
        list[i] = item  # для удобства именования внутри используем item

    list = listF.rmDoublesStr(listF.rmBlankStr(list))
    if type == 'phone' and not list and params['noBlanks']: return G.badPhone
    return ','.join(list)
def getSuggList(type:str,value:str):
    final = []
    if   type in ('mail','website'):
        new  = value.replace(' ','').replace('|',',')
        if new != value:
            vObj = {'type':type,'value':new,'valid':None,'errKey':''}
            validateCell(vObj)
            if vObj['valid']: final.append({'val':new,'btn':new})
    elif type ==  'date':
        parts = trySplitDate(value.strip('00:00:00').strip())
        if parts:
            for        i in range(3):
                for    j in range(3):
                    if i != j:
                        new = parts[i]+'.'+parts[j]+'.'+parts[3-i-j]
                        if validateDate(new): final.append({'val':new,'btn':new})
    return final
def validateCell(vObj:dict,params=None):    # vObj={'type':,'value':,'valid':,'errKey':}
    if   vObj['type'] in ('phone','mail','website'):
        list = vObj['value'].split(',')
        if listF.inclDoublesStr(list,True):
            vObj['valid']  = False
            vObj['errKey'] = 'listDoubles'
            return
        if vObj['type'] == 'phone' and len(list) > 1 and G.badPhone in list:
            vObj['valid']  = False
            vObj['errKey'] = 'nines_inMany'
            return
        for item in list:
            vObj['valid'],vObj['errKey'] = checkPMW(vObj['type'],item,params)
            if not        vObj['valid']: return
        if vObj['type'] in ('mail','website'): vObj['value'] = vObj['value'].lower()
    elif vObj['type'] == 'date':
        vObj['valid'] = validateDate(vObj['value'])
        if not vObj['valid']:
            vObj  ['errKey'] = 'format'
            return
    vObj['valid'] = True
def checkPMW(type:str,value:str,params=None):
    # PMW = phone, mail, website
    # возвращаем valid:True/False и ключ для S.errInput[type]
    if   type == 'phone':
        if not params['noBlanks'] and value    == ''        : return True,''
        if not params['noBlanks'] and value    == G.badPhone: return False,'secNines'
        if                        len(value)   != 11        : return False,'length'
        if                            value[0] != '7'       : return False,'firstSymb'
        if                            value[1] in '67'      : return False,'kazakh'
    elif type == 'mail':
        if value            == ''        : return True ,''
        if value.count('@') != 1         : return False,'dogCount'
        if inclSubList(value,G.ruSymbols): return False,'ru'
        if '$'      in value             : return False,'$'

        name,domain = value.split('@')
        if not     '.' in          domain: return False, 'dotDomain'
        if        '..' in          domain: return False,'dotsDomain'
        if len(domain) > 1 and domain[-2:] in ('.c','.r'): return False,'endDomain'
        if name        in    G.allHyphens: return False, 'hyphen'
        if inclSubList(value,G.badSymbols[type],False,False):
            return False,'badSymbols'
    elif type == 'website':
        if value      ==    '': return True ,''
        if not    '.' in value: return False,'dot'
        if value.endswith('/'): return False,'endSlash'
        if checkStartList(value,G.badWebStarts,'bool'): return False,'wwwHttp'
        if checkStartList(value,G.rmSites     ,'bool'): return False,'rmSites'
        if inclSubList   (value,G.badSymbols[type],False,False):
            return False,'badSymbols'
        if findSub       (value,'?ysclid='    ,'bool'): return False,'yaTrack'

        index = findSub(value,'hh.ru/')
        if index > 0: return False,'hhCity'
    return True,''
def trySplitDate(date:str):
    for symb in G.dateSplitters:
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
            if y in range(2000,2100) and m in range(1,13) and d in range(1,G.monthDays[m]+1): return True
    return False

# исправление регионов/городов; RC = region/city
def ACcity(city:str,regions:list,ACregions:list):
    # ошибка при импорте lib сюда, поэтому передаём аргументами regions и ACregions
    city   =  joinSpaces      (city)
    city   = RCfixOblast      (city)
    city   = RCrmOblast       (city,regions,ACregions)
    city   = RCtrimCity       (city)
    city   = mRCtrims         (city)
    if listF.inclStr(ACregions,city): return city

    city   = lat_toCyr        (city)
    city   = trimOverHyphens  (city)
    city   = RCtry            (city,ACregions)
    return city
def RCfixOblast(city:str):
    list = city.split()
    for  i in range(len(list)):
        if mRCtrims(list[i]).lower() in ('обл','оюл','облость'):
            list[i] = 'область'
            return ' '.join(list)
    return city
def RCrmOblast (city:str,regList:list,ACregions:list):
    initCity  = city
    city      = RCsplitRegion(city,regList)[0]
    city      = RCtrimCity   (city) # только для проверки ACregions, приходится дублировать следующий шаг
    if city and listF.inclStr(ACregions,city): return city
    else:                                      return initCity
def RCsplitRegion(string:str,regList:list):
    # ищет в string каждый регион и, если найдёт его, возвращает отдельно город и регион
    init   = string
    region = findSubList(string,regList)
    if region is not None and len(region) != len(string):
        string = mRCtrims(string.lower().replace(region.lower(),''))
        if not string: string = init
    return string,region
def RCtrimCity (city:str):
    # сначала те, что с пробелом
    list = city.split()
    for i in (0,-1):
        list[i] = list[i].replace('(','').replace(')','')
        if listF.inclStr(G.cTrims['spaced'],list[i]):
            list.pop(i)
            return ' '.join(list)

    # потом           те, что могут быть в начале строки без пробела, но в скобках
    # и сразу за ними те, что могут быть в начале строки без пробела и без скобок
    temp     = rmStartList(city,G.cTrims['start'],1)
    if temp != city: return temp

    return city
def RCtry      (city:str,ACregions:list):
    # пробует заменять 'е'<->'ё' (в обе стороны), все пробелы на дефисы (напр., для 'Ростов на Дону')
    # и подчёркивания на пробелы/дефисы (напр., для 'Санкт_Петербург')
    # возвращает новый вариант, если получится правильный город либо подходящий под автозамену
    RPL   = {'е':'ё','ё':'е'}   # RPL = replacement
    vList =  ACregions
    vars  = [city                 ,
             city.replace(' ','-'),
             city.replace('_','-'),
             city.replace('_',' ')]
    vars  = listF.rmDoublesStr                (vars)
    found = listF.searchAny_from_strList(vList,vars)
    if found is not None: return found

    for   var in vars:
        for i in range(len(var)):
            if var[i] in RPL.keys():
                new = replaceIndex(var,i,RPL[var[i]])
                if   listF.inclStr(vList,new): return new
    return city
def mRCtrims   (city:str):  # main region/city trims
    city = rmStartList(city,G.mrcTrims,0,False)
    while city and city[-1] in G.mrcTrims: city = city[:-1]
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
            new   = item if type == 'item' else result
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
def checkStartList(string:str,list:list,type='item',lower=True,stripList=False):
    # проверяет каждый элемент списка list[]: если он в начале строки, возвращает этот элемент или True/False
    # type может быть 'item' или 'bool'
    for item in list:
        if findSub(string,item,'index',False,lower,('','b')[stripList]) == 0: return (True,item)[type == 'item']
    return (False,None)[type == 'item']

# изменение (общие)
def cut_ifFound    (string:str,sub :str ,side='end',lower=True,strip='',inclSub=False,maxCut=0):
    # ищет sub в string, обрезает начало (side='start') или конец (side='end')
    # inclSub: оставить sub в возвращаемом результате (True) или нет (False)
    # если обрежется больше, чем maxCut, то ничего не делает: вернёт изначальную string
    # maxCut=0 отключает ограничение
    index     = findSub(string,sub,'index',False,lower,strip)
    if index >= 0:
        new             = string[:index] if side == 'end' else string[len(sub)+index:]
        if inclSub: new = new + sub      if side == 'end' else sub + new
    else: return string

    if not maxCut or len(string)-len(new) <= maxCut: return new
    else:                                            return string
def rmStartList    (string:str,list:list,count=0,lower=True,stripList=False):
    # проверяет каждый элемент списка list[]: если он в начале строки, удаляет его из начала строки
    # count = сколько раз удалять; если count=0, удаляем все, пока в начале не будет что-то другое
    iter = 0    # итерация: увеличивается на 1, когда производим удаление
    while count == 0 or (count >= 0 and iter < count):
        found = checkStartList(string,list,'item',lower,stripList)
        if not found: return string
        else:
            string = string.replace(found,'',1)
            iter  += 1
    return string
def joinSpaces     (string:str): # объединяет все мультипробелы в одинарные
    # while быстрее, чем regex и split+join
    string = string.replace(' ',' ')    # заменяем неразрывные пробелы
    while '  ' in string: string = string.replace('  ',' ')
    return string
def lat_toCyr      (string:str):
    for init,to in G.lat_toCyr.items():
        string = string.replace(init        ,to)
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
def capitalize     (string:str,type :str):
    if   type == 'Aa_Aa':
        list = string.split()
        for i  in range(len(list)): list[i] = list[i].capitalize()
        return ' '.join(list)
    elif type == 'Aa_aa': return string.capitalize()
    elif type == 'Aa_aA': return string[0]  .upper() + string[1:]
    elif type == 'AA_AA': return string     .upper()
    elif type == 'aa_aa': return string     .lower()

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
