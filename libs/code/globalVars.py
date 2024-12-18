from sys          import exit as SYSEXIT
from excelRW      import exBooks
from userSettings import userCfg

# базовые переменные приложения
app = {'version': 'v.090',
       'title'  : 'excelALC',
       'themes' : ('flatly','superhero'),           # светлая и тёмная темы
       'size'   : (1000, 600)}
app   ['TV']    = app['title']+' '+app['version']   # название главного окна

# файлы
picsDir = 'libs/pics/'
files   = {'lib'          :'справочник excelALC.xlsx',
           'config'       : app['title']+       '.config',
           'log'          : app['title']+  ' main.log',
           'errors'       : app['title']+' errors.log'}
pics    = {# нельзя здесь создавать PhotoImage: нужен master-объект
    'filesUpdate'  :  picsDir                 +'filesUpdate.png',
    'themeSelector':{'light': {'pic' :picsDir + 'themeLight.png',
                               'side':'left',
                               'padx':4},
                     'dark' : {'pic' :picsDir + 'themeDark.png',
                               'side':'right',
                               'padx':0}}
    }

# настройки
config = userCfg(files['config'])

# цвета (разные для светлой[0] и тёмной[1] тем; colors перезаписывается при смене темы)
themeColors = ( # ↓ светлая
               {'blue'    :'#277CD4',
                'green'   :'#4AAC7F',
                'magenta' :'#936BCC',
                'pink'    :'#D22E9E',
                'red'     :'#DE3923',
                'lightRed':'#E36B4F',
                'sand'    :'#D1A63E'},
                # ↓ тёмная
               {'blue'    :'#7BBCFF',
                'green'   :'#8EE4BD',
                'magenta' :'#C4ABE7',
                'pink'    :'#FBA1DE',
                'red'     :'#EF6C32',
                'lightRed':'#E36F47',
                'sand'    :'#FFE5A7'})  # аналог lightYellow
exColors    =  {'goodTitle':'#56E0AB',
                'hlChanged':'#E8E782',  # hl = highlight (cell)
                'hlError'  :'#F69A98'}
colors = themeColors[config.get('main:darkTheme')]
colors.update(exColors)

# параметры по типам скриптов
launchTypes = {
    'allChecks'    :{'readRange'  :'shActive',
                     'toTD'       : True,
                     'addHeader'  : True,   # кол-во ошибок и уникальных; нужно только при toTD=True
                     'launch'     :'allChecks',
                     'justVerify' : False,
                     'resetBg'    :'sheet', # сбросить цвета ячеек на листе/в первой строке/в range/нигде
                     'hlTitles'   : True,   # менять ли подсветку заголовков столбцов
                     'getOnLaunch':[],      # читаем при запуске
                     # ↓ какие настройки прочитать из userCfg
                     'getUserCfg' :['suggestErrors','reorder']},    # с tuple'ами почему-то не работает
    'reCalc'       :{'readRange'  :'shActive',
                     'toTD'       : True,
                     'addHeader'  : True,
                     'launch'     :'reCalc',
                     'justVerify' : True,
                     'resetBg'    :'sheet',
                     'hlTitles'   : True,
                     'getOnLaunch':[],
                     'getUserCfg' :[]},
    'checkTitles'  :{'readRange'  :'shActive',
                     'toTD'       : True,
                     'addHeader'  : False,
                     'launch'     :'checkTitles',
                     'justVerify' : False,
                     'resetBg'    :'sheet',
                     'hlTitles'   : True,
                     'getOnLaunch':[],
                     'getUserCfg' :['suggestErrors','reorder'],
                     # ↓ тип проверки для autocorr & suggest (нужен не везде)
                     'AStype'     :'title'},
    'checkCities'  :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'rangeChecker',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['suggestErrors'],
                     'AStype'     :'region'},
    'checkCat'     :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'rangeChecker',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['suggestErrors'],
                     'AStype'     :'cat'},
    'checkVert'    :{'readRange'  :'shSelection',
                     'toTD'       : False,
                     'launch'     :'checkVert',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['autocorr','onlyBlanks'],
                     'AStype'     :'vert'},
    'checkSources' :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'rangeChecker',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['suggestErrors'],
                     'AStype'     :'source'},
    'checkPhones'  :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'rangeChecker',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['noBlanks'],
                     'AStype'     :'phone'},
    'checkEmails'  :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'rangeChecker',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['suggestErrors'],
                     'AStype'     :'mail'},
    'checkWebsites':{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'rangeChecker',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['suggestErrors'],
                     'AStype'     :'website'},
    'checkDates'   :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'rangeChecker',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['suggestErrors'],
                     'AStype'     :'date'},
    'rmEmptyRC'    :{'readRange'  :'shActive',
                     'toTD'       : False,
                     'launch'     :'rmEmptyRC',
                     'justVerify' : False,
                     'resetBg'    :'sheet',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['rmTitled']},
    'capitalize'   :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'capitalize',
                     'justVerify' : False,
                     'resetBg'    :'selection',
                     'hlTitles'   : False,
                     'getOnLaunch':[],
                     'getUserCfg' :['selected']},
    'fillBlanks'   :{'readRange'  :'selection',
                     'toTD'       : False,
                     'launch'     :'fillBlanks',
                     'justVerify' : False,
                     'resetBg'    :'none',
                     'hlTitles'   : False,
                     'getOnLaunch':['filler'],
                     'getUserCfg' :['filler']}
    }

# readLib   : прочитать подходящие варианты для валидации из библиотеки
# checkList : валидация путём проверки, есть ли value в списке допустимых (extra)
# showSugg  : предлагать ли исправить
# getLibSugg: варианты исправления надо прочитать из библиотеки; иначе берём из strF.getSuggList()
# (не нужно?) acceptBlank: для диалога с предложением исправить (None означает, что надо прочитать из настроек)
# ↓ !БОЛЬШИНСТВО ЭТИХ ТИПОВ ДОЛЖНО БЫТЬ В strings.suggMsg! ↓
AStypes = {'title'  :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
           'region' :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
           'cat'    :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
           'vert'   :{'readLib':False,'checkList':True ,'showSugg':False,'getLibSugg':True},
           'source' :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
           'phone'  :{'readLib':False,'checkList':False,'showSugg':False,'getLibSugg':False},
           'mail'   :{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False},
           'website':{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False},
           'date'   :{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False}}

log = {
    'units' :{'mainLaunch'     :'core',
              'launchType'     :'core',     # отсутствует в S.log: читается из S.layout
              'readSheet'      :'core',
              'readFile'       :'core',
              'ACsuccess'      :'autocorr', # используется и при запуске capitalize
              'errorsFound'    :'errors',
              'suggFinished'   :'sugg',
              'columnAdded'    :'titles',
              'titlesReordered':'titles',
              'RCremoved'      :'rmRC',
              'vertChanged'    :'warning',
              'blanksFilled'   :'autocorr',
              'finalWrite'     :'finalWrite',
              'colorErrors'    :'finalWrite',
              'fileSaved'      :'finalWrite'},
    'colors':{'core'           : None,
              'autocorr'       :'sand',
              'capitalize'     :'sand',
              'errors'         :'red',
              'rmRC'           :'pink',
              'warning'        :'red',
              'sugg'           :'magenta',
              'titles'         :'blue',
              'finalWrite'     :'green'}
    }

# прочее
exBooks = exBooks()

# особые символы
# ↓ неподходящие для почты и сайта
badSymbols    = {'mail'   :(':','|','/','’',' ','<','>','[',']','.@','@.','@-.'),
                 'website':(' ','@','|')}
badWebStarts  = ('http://'  ,'https://'  ,'www.')
badPhone      = '79999999999'
rmSites       = ('facebook.','instagram.' ,'twitter.')
initRegList   = ['Россия'   ,'все регионы','другие регионы','другой регион']

allHyphens    = ['-','–','—']
ruSymbols     = ('а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п',
                 'р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я')

dateSplitters = ['/'] + allHyphens
monthDays     = {1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

# cTrims = city trims; 'noSpace' нужен только здесь для расстановки всех вариантов
cTrims  = {'noSpace':['г.','д.','п.','с.','х.','рп.','дп.','ст.','пос.','пгт.','гор.','городской пос.'],
           'spaced' :['г' ,'д' ,'п' ,'с' ,'х' ,'рп' ,'дп' ,'ст' ,'посёлок','поселок','пос','пгт',
                      'гор','городской пос','город','станица','ст-ца','хутор', 'село','деревня']}
cTrims    ['spaced'] = cTrims['noSpace'] + cTrims['spaced']
cTrims    ['start']  = ['('+item+')' for item in cTrims['spaced']] + cTrims['noSpace']
cTrims.pop('noSpace')

# main region/city trims (только начало/конец строки)
# ЦИФРЫ НЕ ДОБАВЛЯТЬ! (будут ошибки типа "МСК+2" -> "Москва")
mrcTrims = (' ','.',',','(',')','/','|','\\','?','!','+','-','–','—')

# преобразование латиницы в кириллицу
lat_toCyr = {'Ch':'Ч' ,"Kh'":'Хь','Kh’':'Хь','Kh':'Х' ,'Sh':'Ш' ,'Ts':'Ц' ,
             'Ay':'Ай','Ey' :'Ей','Iy' :'Ий','Yy':'Ый','Ya':'Я' ,'Ye':'Е' ,'Yo':'Е','Yu':'Ю','Zh':'Ж',
             "L'":'Ль','L’' :'Ль',"N'" :'Нь','N’':'Нь',"T'":'Ть','T’':'Ть',
             'A' :'А' ,'B'  :'Б' ,'D'  :'Д' ,'E' :'Е' ,'F' :'Ф' ,'G' :'Г' ,'H' :'Х','I' :'И',
             'K' :'К' ,'L'  :'Л' ,'M'  :'М' ,'N' :'Н' ,'O' :'О' ,'P' :'П' ,'R' :'Р',
             'S' :'С' ,'T'  :'Т' ,'U'  :'У' ,'V' :'В' ,'W' :'В' ,'Y' :'Ы' ,'Z' :'З'}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
