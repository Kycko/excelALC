from   sys         import exit as SYSEXIT
from   globalFuncs import getIB
import globalsMain      as G

# поиск (общие)
def findSub       (string:str,sub:str,type='index',fullText=False,lower=True,strip=''):
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
def findSubList   (string:str,list:list,type='item',multi=False,fullText=False,lower=True,strip=''):
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
def checkStartList(string:str,list:list,type='item',lower=True,stripList=False):
    # проверяет каждый элемент списка list[]: если он в начале строки, возвращает найденное или True/False
    # type может быть 'item' или 'bool'
    for item in list:
        if findSub(string,item,'index',False,lower,('','b')[stripList]) == 0:
            return string[:len(item)] if type == 'item' else True
    return (False,None)[type == 'item']

# изменение (общие)
def rmStartList(string:str,list:list,count=0,lower=True,stripList=False):
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
def joinSpaces (string:str):    # объединяет все мультипробелы в одинарные
    # while быстрее, чем regex и split+join
    string = string.replace(' ',' ')    # заменяем неразрывные пробелы
    while '  ' in string: string = string.replace('  ',' ')
    return string

# исправление регионов/городов; RC = region/city
def RCfixOblast  (city:str):
    list = city.split()
    for  i in range(len(list)):
        if mRCtrims(list[i]).lower() in ('обл','оюл','облость'):
            list[i] = 'область'
            return ' '.join(list)
    return city
def RCsplitRegion(string:str,regList:list):
    # ищет в string каждый регион и, если найдёт его, возвращает отдельно город и регион
    init   = string
    region = findSubList(string,regList)
    if region is not None and len(region) != len(string):
        string = mRCtrims(string.lower().replace(region.lower(),''))
        if not string: string = init
    return string,region
def mRCtrims     (city:str):    # main region/city trims
    city = rmStartList(city,G.mrcTrims,0,False)
    while city and city[-1] in G.mrcTrims: city = city[:-1]
    return city

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
