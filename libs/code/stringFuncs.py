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

# проверка и исправление данных
def autocorrCell(type:str,value:str):
    if type == 'mail': return ACmail(value)
    else:              return        value
def ACmail(value:str):
    value = value.lower()
    RPL   = {'from': ('​','–','—','|',';','; ',', ',',,'),  # RPL = replace
             'to'  : ('','-','-',',',',',',' ,',' ,',' )}
    for i in range(len(RPL['from'])): value = value.replace(RPL['from'][i],RPL['to'][i])

    list = value.split(',')
    for i in range(len(list)):
        parts = list[i].split('@')
        if 'gmail' in parts[-1]: parts[-1] = 'gmail.com'
        list[i] = '@'.join(parts)

    return ','.join(listF.rmDoublesStr(list))
def getSuggList(type:str,value:str):
    if type == 'mail':
        new = value.replace(' ','')
        if new != value and checkMail(new): return [new]
    return []
def validateCell(type:str,value:str):
    if type in ('phone','mail','website'):
        # ПО ТЕЛЕФОНАМ ПОТОМ ДОПИСАТЬ, ДОПОЛНИТЕЛЬНЫЕ МОГУТ БЫТЬ ПУСТЫМИ И НЕ МОГУТ БЫТЬ 79999999999
        for item in value.split(','):
            if   type == 'phone'   and not checkPhone  (item): return False
            elif type == 'mail'    and not checkMail   (item): return False
            elif type == 'website' and not checkWebsite(item): return False
    return True
def checkPhone(phone:str):
    if len(phone) != 11  : return False
    if phone[0]   != '7' : return False
    if phone[1]   in '67': return False # казахские номера
    return True
def checkMail(mail:str):
    if mail             == ''       : return True
    if mail .count('@') != 1        : return False
    if findSubList(mail,G.ruSymbols): return False

    name,domain = mail.split('@')
    if not     '.' in       domain: return False
    if        '..' in       domain: return False
    if domain[-2:] in  ('.c','.r'): return False # аналог endswith()
    if name        in G.allHyphens: return False
    if findSubList(mail,(':','|','/','’',' ','<','>','[',']','.@','@.','@-.'),'bool',False,False,False): return False
    return True
def checkWebsite(site:str):
    if site       ==   '': return True
    if not    '.' in site: return False
    if site.endswith('/'): return False
    if findSubList(site,(' ','@','|'),     'bool',False,False)     : return False
    if findSubList(site,('http://','https://','www.'),'index') == 0: return False
    return True

# поиск
def findSubList(string:str,list:list,type='bool',fullText=False,lower=True,stripList=True):
    # ищет в строке каждый элемент списка; type может быть 'index', 'bool' и 'item'
    # индекс – это позиция найденного в string, 'item' вернёт найденный элемент списка list
    for item in list:
        result = findSub(string,item,'index',fullText,lower,stripList)
        if result >= 0: return item if type == 'item' else getIB(type,result)
    return None if type == 'item' else getIB(type,-1)
def findSub(string:str,sub:str,type='index',fullText=False,lower=True,stripSub=True):
    # type может быть 'index' или 'bool'
    # если fullText=True, проверяется равенство строк (но после .trim() + можно задать lower=True)
    # если lower   =True, все строки будут сравниваться через .toLowerCase()
    string           = string.strip()
    if stripSub: sub = sub   .strip()

    if fullText and len(string) != len(sub): return getIB(type,-1)
    if lower:
        string = string.lower()
        sub    = sub   .lower()

    return getIB(type,string.find(sub))

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
