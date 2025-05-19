from   sys import exit as SYSEXIT
import dictFuncs       as dictF

class globDicts():  # импортируется в G.dict (в глобальные переменные)
  def __init__(self):
    # эти свойства записываются в rootClasses.pr{} (properties)
    def _taskShared(type:str,upd={}):
      # функция, передающая в self.tasks одинаковые свойства для однотипных элементов
      if type == 'cfg': return ['newSheet','suggErrors','saveAfter']
      else:
        dict = {'chk':{'cfg'        :_taskShared('cfg'),
                       'read'       :'selection',
                       'rmRC_onRead': False,
                       'toTD'       : False,
                       'addHeader'  : False,
                       'launch'     :'rangeChecker',
                       'justVerify' : False,
                       'resetBg'    :'selection',
                       'hlTitles'   : False,
                       'hlVerts'    : False}}
        return dictF.update(dict[type],**upd)
    self.tasks = {# 'chkAll'  :,
                  'chkCat'  :_taskShared('chk',{'root':{'AStype':'cat'}}),
                  'chkSrc'  :_taskShared('chk',{'root':{'AStype':'source'}}),
                  'chkMails':_taskShared('chk',{'root':{'AStype':'mail'}}),
                  'rmRC'    :{'cfg'        :['newSheet',
                                             'saveAfter',
                                             '---',   # будет просто separator
                                             'rmTitled'],
                              'read'       : 'shActive',
                              'rmRC_onRead':  False,  # это для toTD?
                              'toTD'       :  False,
                              'addHeader'  :  False,
                              'launch'     : 'rmRC',
                              'justVerify' :  False,
                              'resetBg'    : 'sheet',
                              'hlTitles'   :  False,
                              'hlVerts'    :  False}}

    self.log = {'mainLaunch'      :'core',
                'launchType'      :'core',
                'readSheet'       :'core',
                'readRange:full'  :'core',
                'readRange:range' :'core',
                'ACsuccess'       :'autocorr',
                'errorsFound'     :'errors',
                'sugg+'           :'sugg',
                'sugg-'           :'sugg',
                'columnAdded'     :'titles',
                'titlesReordered' :'titles',
                'RCremoved'       :'rmRC',
                'vertChanged'     :'warning',
                'blanksFilled'    :'autocorr',
                'finalWrite+'     :'finalWrite',
                'finalWrite-'     :'finalWrite',
                'finalColors_0'   :'finalWrite',
                'finalColors_done':'finalWrite',
                'finalColors_skip':'finalWrite',
                'fileSaved'       :'finalWrite'}

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
    self.colLetters =  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    self.exColors   = {'goodTitle':'#56E0AB', # ex = Excel
                       'hlChanged':'#E8E782', # hl = highlight (cell)
                       'hlError'  :'#F69A98'}

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
    self.strips     = {'cat':('.','-','|')} # какие символы отрезаем autocorr'ом

    self.dateSplitters = ['/'] + self.allHyphens
    self.monthDays  = {1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

    # cTrims = city trims; 'noSpace' нужен только здесь для расстановки всех вариантов
    cTrims  = {'noSpace':['г.','д.','п.','с.','х.','рп.','дп.',
                          'ст.','пос.','пгт.','гор.','городской пос.'],
               'spaced' :['г','д','п','с','х','рп','дп','ст','посёлок','поселок',
                          'пос','пгт','гор','городской пос','город','станица',
                          'ст-ца','хутор','село','деревня']}
    cTrims    ['spaced'] = cTrims['noSpace'] + cTrims['spaced']
    cTrims    ['start']  = ['('+item+')' for item in cTrims['spaced']] + cTrims['noSpace']
    cTrims.pop('noSpace')
    self.cTrims = cTrims

    # main region/city trims (только начало/конец строки)
    # ЦИФРЫ НЕ ДОБАВЛЯТЬ! (будут ошибки типа "МСК+2" -> "Москва")
    self.mrcTrims = (' ','.',',','(',')','/','|','\\','?','!','+','-','–','—')

    # преобразование латиницы в кириллицу
    self.lat_toCyr = {
      'Ch':'Ч',"Kh'":'Хь','Kh’':'Хь','Kh':'Х','Sh':'Ш','Ts':'Ц','Ay':'Ай',
      'Ey':'Ей','Iy':'Ий','Yy':'Ый','Ya':'Я','Ye':'Е','Yo':'Е','Yu':'Ю',
      'Zh':'Ж',"L'":'Ль','L’':'Ль',"N'":'Нь','N’':'Нь',"T'":'Ть','T’':'Ть',
      'A':'А','B':'Б','D':'Д','E':'Е','F':'Ф','G':'Г','H':'Х','I':'И',
      'K':'К','L':'Л','M':'М','N':'Н','O':'О','P':'П','R':'Р','S':'С',
      'T':'Т','U':'У','V':'В','W':'В','Y':'Ы','Z':'З'
      }

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
