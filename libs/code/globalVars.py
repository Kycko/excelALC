from sys          import exit as SYSEXIT
from excelRW      import exBooks
from userSettings import userCfg

# базовые переменные приложения
app = {'version': 'v.043',
       'title'  : 'excelALC',
       'themes' : ('flatly','superhero'),           # светлая и тёмная темы
       'size'   : (1000, 600)}                      # при необходимости добавим в другой переменной размеры диалоговых окон
app   ['TV']    = app['title']+' '+app['version']   # название главного окна

# файлы
picsDir = 'libs/pics/'
files   = {'lib'          :'справочник excelALC.xlsx',
           'config'       : app['title']+       '.config',
           'log'          : app['title']+  ' main.log',
           'errors'       : app['title']+' errors.log'}
pics    = {'filesUpdate'  : picsDir     +'filesUpdate.png', # нельзя здесь создавать PhotoImage, т. к. нужен master-объект
           'themeSelector':{'light': {'pic' :picsDir+'themeLight.png',
                                      'side':'left',
                                      'padx':4},
                            'dark' : {'pic' :picsDir+'themeDark.png',
                                      'side':'right',
                                      'padx':0}}}

# настройки
config = userCfg(files['config'])

# цвета (разные для светлой[0] и тёмной[1] тем; colors перезаписывается при смене темы)
themeColors = ( # ↓ светлая
               {'green'   :'#4AAC7F',
                'magenta' :'#936BCC',
                'red'     :'#DE3923',
                'lightRed':'#E36B4F',
                'sand'    :'#D1A63E'},
                # ↓ тёмная
               {'green'   :'#8EE4BD',
                'magenta' :'#C4ABE7',
                'red'     :'#EF6C32',
                'lightRed':'#E36F47',
                'sand'    :'#FFE5A7'})  # аналог lightYellow
exColors    =  {'hlError' :'#F69A98'}   # hl = highlight (cell)
colors = themeColors[config.get('main:darkTheme')]
colors.update(exColors)

# параметры по типам скриптов
# getUserCfg = какие настройки прочитать из userCfg; можно этот ключ не указывать (с tuple'ами почему-то не работает)
# AStype (нужен не везде) = тип проверки для autocorr & suggest
launchTypes = {
    'allChecks'    :{'readRange':'shActive', 'toTD':True ,'launch':'allChecks'   ,'justVerify':False,'getUserCfg':['suggestErrors']},
    'checkTitles'  :{'readRange':'shActive', 'toTD':True ,'launch':'checkTitles' ,'justVerify':False,'getUserCfg':['suggestErrors'],'AStype':'title'},
    'checkCities'  :{'readRange':'selection','toTD':False,'launch':'rangeChecker','justVerify':False,'getUserCfg':['suggestErrors'],'AStype':'region'},
    'checkPhones'  :{'readRange':'selection','toTD':False,'launch':'rangeChecker','justVerify':False,'getUserCfg':['noBlanks']     ,'AStype':'phone'},
    'checkEmails'  :{'readRange':'selection','toTD':False,'launch':'rangeChecker','justVerify':False,'getUserCfg':['suggestErrors'],'AStype':'mail'},
    'checkWebsites':{'readRange':'selection','toTD':False,'launch':'rangeChecker','justVerify':False,'getUserCfg':['suggestErrors'],'AStype':'website'}
    }

# readLib   : прочитать подходящие варианты для валидации из библиотеки
# checkList : валидация путём проверки, есть ли value в списке допустимых (extra)
# showSugg  : предлагать ли исправить
# getLibSugg: варианты исправления надо прочитать из библиотеки; иначе берём из strF.getSuggList()
# (не нужно?) acceptBlank: для диалога с предложением исправить (None означает, что надо прочитать из настроек)
# ↓ !ВСЕ ЭТИ ТИПЫ ДОЛЖНЫ БЫТЬ В strings.suggMsg! ↓
AStypes = {'title'  :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
           'region' :{'readLib':True ,'checkList':True ,'showSugg':True ,'getLibSugg':True},
           'phone'  :{'readLib':False,'checkList':False,'showSugg':False,'getLibSugg':False},
           'mail'   :{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False},
           'website':{'readLib':False,'checkList':False,'showSugg':True ,'getLibSugg':False}}

log = {'units' :{'mainLaunch'  :'core',
                 'launchType'  :'core', # отсутствует в S.log: читается из S.layout
                 'readSheet'   :'core',
                 'readFile'    :'core',
                 'ACsuccess'   :'autocorr',
                 'errorsFound' :'errors',
                 'suggFinished':'sugg',
                 'finalWrite'  :'finalWrite',
                 'colorErrors' :'finalWrite',
                 'fileSaved'   :'finalWrite'},
       'colors':{'core'        : None,
                 'autocorr'    :'sand',
                 'errors'      :'red',
                 'sugg'        :'magenta',
                 'finalWrite'  :'green'}}

# прочее
exBooks = exBooks()

# особые символы
# ↓ неподходящие для почты и сайта
badSymbols   = {'mail'   :(':','|','/','’',' ','<','>','[',']','.@','@.','@-.'),
                'website':(' ','@','|')}
badWebStarts = ('http://'  ,'https://'  ,'www.')
badPhone     = '79999999999'
rmSites      = ('facebook.','instagram.' ,'twitter.')
initRegList  = ['Россия'   ,'все регионы','другие регионы','другой регион']

allHyphens   = ('-','–','—')
ruSymbols    = ('а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п',
                'р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я')

# cTrims = city trims; 'noSpace' нужен только здесь для расстановки всех вариантов
cTrims  = {'noSpace':['г.','д.','с.','х.','рп.','дп.','ст.','пос.','пгт.','городской пос.'],
           'spaced' :['г' ,'д' ,'с' ,'х' ,'рп' ,'дп' ,'ст' ,'посёлок','поселок','пос','пгт',
                      'городской пос','город','станица','ст-ца','хутор', 'село','деревня']}
cTrims    ['spaced'] = cTrims['noSpace'] + cTrims['spaced']
cTrims    ['start']  = ['('+item+')' for item in cTrims['spaced']] + cTrims['noSpace']
cTrims.pop('noSpace')

# преобразование латиницы в кириллицу
lat_toCyr = {'Ch':'Ч' ,"Kh'":'Хь','Kh’':'Хь','Kh':'Х' ,'Sh':'Ш' ,'Ts':'Ц' ,
             'Ay':'Ай','Ey' :'Ей','Iy' :'Ий','Yy':'Ый','Ya':'Я' ,'Ye':'Е' ,'Yo':'Е','Yu':'Ю','Zh':'Ж',
             "L'":'Ль','L’' :'Ль',"N'" :'Нь','N’':'Нь',"T'":'Ть','T’':'Ть',
             'A' :'А' ,'B'  :'Б' ,'D'  :'Д' ,'E' :'Е' ,'F' :'Ф' ,'G' :'Г' ,'H' :'Х','I' :'И','K' :'К','L':'Л','M':'М',
             'N' :'Н' ,'O'  :'О' ,'P'  :'П' ,'R' :'Р' ,'S' :'С' ,'T' :'Т' ,'U' :'У','V' :'В','W' :'В','Y':'Ы','Z':'З'}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
