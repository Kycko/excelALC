from   sys import exit as SYSEXIT
import dictFuncs       as dictF

class globDicts():  # импортируется в G.dict (в глобальные переменные)
  def __init__(self):
    # эти свойства записываются в rootClasses.pr{} (properties)
    def _taskShared(type:str,upd={}):
      # функция, передающая в self.tasks одинаковые свойства для однотипных элементов
      if type == 'cfg': return ['newSheet','suggErrors','confirmWrite','saveAfter']
      else:
        dict = {'chk':{'cfg'       :_taskShared('cfg'),
                       'read'      :'selection',
                       'toTD'      : False,
                       'addHeader' : False,
                       'launch'    :'rangeChecker',
                       'justVerify': False,
                       'resetBg'   :'selection',
                       'hlTitles'  : False}}
        return dictF.update(dict[type],**upd)

    self.tasks = {'chkCat':_taskShared('chk',{'root':{'AStype':'cat'}}),
                  'chkSrc':_taskShared('chk',{'root':{'AStype':'source'}})}

    self.log   = {'units' :{'mainLaunch'     : 'core',
                            'launchType'     : 'core',  # отсутствует в S.log: читается из S.UI['tasks]
                            'readSheet'      : 'core',
                            'readFile'       : 'core',
                            'ACsuccess'      : 'autocorr',  # используется и при запуске capitalize
                            'errorsFound'    : 'errors',
                            'suggFinished'   : 'sugg',
                            'columnAdded'    : 'titles',
                            'titlesReordered': 'titles',
                            'RCremoved'      : 'rmRC',
                            'vertChanged'    : 'warning',
                            'blanksFilled'   : 'autocorr',
                            'finalWrite'     : 'finalWrite',
                            'colorErrors'    : 'finalWrite',
                            'fileSaved'      : 'finalWrite'},
                  'files' :{'core'           :('main','changes','errors')},
                  'colors':{'core'           :  None,
                            'autocorr'       : 'sand',
                            'capitalize'     : 'sand',
                            'errors'         : 'red',
                            'rmRC'           : 'pink',
                            'warning'        : 'red',
                            'sugg'           : 'magenta',
                            'titles'         : 'blue',
                            'finalWrite'     : 'green'}}

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
