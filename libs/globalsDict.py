from   sys import exit as SYSEXIT
import dictFuncs       as dictF

class globDicts():  # импортируется в G.dict (в глобальные переменные)
  def __init__(self):
    # эти свойства записываются в rootClasses.pr{} (properties)
    def _getShared(type:str,upd={}):
      # функция, передающая в self.tasks одинаковые свойства для однотипных элементов
      if type == 'cfg': return ['newSheet','suggErrors','confirmWrite','saveAfter']
      else:
        dict = {'chk':{'cfg'       :_getShared('cfg'),
                       'read'      :'selection',
                       'toTD'      : False,
                       'addHeader' : False,
                       'launch'    :'rangeChecker',
                       'justVerify': False,
                       'resetBg'   :'selection',
                       'hlTitles'  : False}}
        return dictF.update(dict[type],**upd)

    self.tasks = {'chkCat':_getShared('chk',{'root':{'AStype':'cat'}}),
                  'chkSrc':_getShared('chk',{'root':{'AStype':'source'}})}

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
