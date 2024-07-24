from   sys         import exit as SYSEXIT
from   globalFuncs import getIB
import globalVars  as G
import listFuncs   as listF

# получение правильного окончания в зависимости от количества
def getEnding_forCount(words:dict,count:int):
    # примеры words есть в words_byCount (модуль strings)
    ten   = count % 10  # остаток деления
    hundr = count % 100 # остаток деления
    if   ten == 0 or ten > 4 or hundr in range(11,15): return words['many']
    elif ten == 1:                                     return words['1']
    else:                                              return words['2-4']

# проверка и исправление разных пользовательских данных
def autocorrCell(type:str,value:str,params=None):
    value = value.strip()
    if type in ('phone','mail','website'): return AC_PMW(type,value,params)
    else:                                  return             value
def AC_PMW(type:str,value:str,params=None): # AutoCorr Phone,Mail,Website
    RPL = {'from': ('​','–','—','|',';',',,'),  # RPL = replace
           'to'  : ('','-','-',',',',',',' )}
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
        list[i] = item  # для удобства именования внутри используем item

    list = listF.rmDoublesStr(listF.rmBlankStr(list))
    if type == 'phone' and not list and params['noBlanks']: return G.badPhone
    return ','.join(list)
def getSuggList(type:str,value:str):
    if type in ('mail','website'):
        new  = value.replace(' ','').replace('|',',')
        if new != value:
            vObj = {'type':type,'value':new,'valid':None,'errKey':''}
            validateCell(vObj)
            if vObj['valid']: return [new]
    return []
def validateCell(vObj:dict,params=None):    # vObj={'type':,'value':,'valid':,'errKey':}
    if vObj['type'] in ('phone','mail','website'):
        # ПО ТЕЛЕФОНАМ ПОТОМ ДОПИСАТЬ, ДОПОЛНИТЕЛЬНЫЕ МОГУТ БЫТЬ ПУСТЫМИ И НЕ МОГУТ БЫТЬ 79999999999
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
        if findSubList(value,G.ruSymbols): return False,'ru'

        name,domain = value.split('@')
        if not     '.' in          domain: return False, 'dotDomain'
        if        '..' in          domain: return False,'dotsDomain'
        if len(domain) > 1 and domain[-2:] in ('.c','.r'): return False,'endDomain'
        if name        in    G.allHyphens: return False, 'hyphen'
        if findSubList(value,G.badSymbols[type],'bool',False,False):
            return False,'badSymbols'
    elif type == 'website':
        if value      ==    '': return True ,''
        if not    '.' in value: return False,'dot'
        if value.endswith('/'): return False,'endSlash'
        if checkStartList(value,G.badWebStarts,'bool'): return False,'wwwHttp'
        if checkStartList(value,G.rmSites     ,'bool'): return False,'rmSites'
        if findSubList   (value,G.badSymbols[type],'bool',False,False):
            return False,'badSymbols'
    return True,''

# поиск (общие)
def findSubList(string:str,list:list,type='bool',fullText=False,lower=True,strip=''):
    # ищет в строке каждый элемент списка list[]; type может быть 'index', 'bool' и 'item'
    # индекс – это позиция найденного в string, 'item' вернёт найденный элемент списка list
    for item in list:
        result = findSub(string,item,'index',fullText,lower,strip)
        if result >= 0: return item if type == 'item' else getIB(type,result)
    return None if type == 'item' else getIB(type,-1)
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
def rmStartList(string:str,list:list,count=0,lower=True,stripList=False):
    # проверяет каждый элемент списка list[]: если он в начале строки, удаляет его из начала строки
    # count = сколько раз удалять; если count=0, удаляем все, пока в начале не будет что-то другое
    iter = 0    # итерация: увеличивается на 1, когда производим удаление
    while checkStartList(string,list,'bool',lower,stripList) and (count == 0 or iter < count):
        string = string.replace(checkStartList(string,list,'item',lower,stripList),'',1)
        iter  += 1
    return string

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
