from   sys import exit as SYSEXIT
import dictFuncs       as dictF

class globDicts():  # импортируется в G.dict (в глобальные переменные)
  def __init__(self):
    # эти свойства записываются в rootClasses.pr{} (properties)
    def _taskShared(type:str,upd={}):
      # функция, передающая в self.tasks одинаковые свойства для однотипных элементов
      if type == 'cfg': return ['newSheet','suggErrors','confirmWrite','saveAfter']
      else:
        dict = {'chk':{'cfg'        :_taskShared('cfg'),
                       'read'       :'selection',
                       'rmRC_onRead': False,
                       'toTD'       : False,
                       'addHeader'  : False,
                       'launch'     :'rangeChecker',
                       'justVerify' : False,
                       'resetBg'    :'selection',
                       'hlTitles'   : False}}
        return dictF.update(dict[type],**upd)
    self.tasks = {'chkCat':_taskShared('chk',{'root':{'AStype':'cat'}}),
                  'chkSrc':_taskShared('chk',{'root':{'AStype':'source'}})}

    self.log = {'mainLaunch'     :'core',
                'launchType'     :'core',
                'readSheet'      :'core',
                'readRange:full' :'core',
                'readRange:range':'core',
                'ACsuccess'      :'autocorr',
                'errorsFound'    :'errors',
                'suggCancelled'  :'sugg',
                'suggAccepted'   :'sugg',
                'columnAdded'    :'titles',
                'titlesReordered':'titles',
                'RCremoved'      :'rmRC',
                'vertChanged'    :'warning',
                'blanksFilled'   :'autocorr',
                'finalWrite'     :'finalWrite',
                'colorErrors'    :'finalWrite',
                'fileSaved'      :'finalWrite'}

    #   readLib : прочитать подходящие варианты для валидации из библиотеки
    #  checkList: валидация путём проверки, есть ли value в списке допустимых (extra)
    #   showSugg: предлагать ли исправить
    # getLibSugg: варианты исправления надо прочитать из библиотеки; иначе берём из strF.getSuggList()
    # (не нужно?) acceptBlank: для диалога с предложением исправить (None означает, что надо прочитать из настроек)
    # ↓ !БОЛЬШИНСТВО ЭТИХ ТИПОВ ДОЛЖНО БЫТЬ В S.suggMsg!
    self.AStypes = {
      'title'  :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
      'region' :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
      'cat'    :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
      'vert'   :{'readLib':False,'checkList':True ,'showSugg':False,'getLibSugg':True},
      'source' :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
      'phone'  :{'readLib':False,'checkList':False,'showSugg':False,'getLibSugg':False},
      'mail'   :{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False},
      'website':{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False},
      'date'   :{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False}
      }

    # разные мелочи
    # ↓ неподходящие для почты и сайта
    self.badSymbols   = {'mail'   :(':','|','/','’',' ','<','>','[',']','.@','@.','@-.'),
                         'website':(' ','@','|')}
    self.badWebStarts = ('http://','https://','www.')
    self.badPhone     =  '79999999999'
    self.rmSites      = ('facebook.','instagram.','twitter.')

    self.allHyphens = ['-','–','—']
    self.ruSymbols  = ('а','б','в','г','д','е','ё','ж','з','и','й',
                       'к','л','м','н','о','п','р','с','т','у','ф',
                       'х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я')

    self.monthDays  = {1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
