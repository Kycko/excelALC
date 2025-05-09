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
        if not '.' in dom: return False, 'dotDomain'
        if    '..' in dom: return False,'dotsDomain'
        if len(dom) > 1 and dom[-2:] in ('.c','.r'): return False,'endDomain'
        if name        in    G.dict.allHyphens: return False,'hyphen'
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

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
