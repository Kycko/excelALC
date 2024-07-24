from sys          import exit as SYSEXIT
from excelRW      import exBooks
from userSettings import userCfg

# базовые переменные приложения
app = {'version': 'v.039',
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
               {'magenta' :'#936BCC',
                'red'     :'#DE3923',
                'lightRed':'#E36B4F',
                'sand'    :'#D1A63E'},
                # ↓ тёмная
               {'magenta' :'#C4ABE7',
                'red'     :'#EF6C32',
                'lightRed':'#E36F47',
                'sand'    :'#FFE5A7'})  # аналог lightYellow
exColors    =  {'hlError' :'#F69A98'}   # hl = highlight (cell)
colors = themeColors[config.get('main:darkTheme')]
colors.update(exColors)

# параметры по типам скриптов
# getSuggParam = надо ли прочитать из userCfg настройку suggestErrors
# AStype (нужен не везде) = тип проверки для autocorr & suggest
launchTypes = {
    'allChecks'    :{'readRange':'shActive', 'toTD':True ,'launch':'allChecks'   ,'justVerify':False,'getSuggParam':True},
    'checkTitles'  :{'readRange':'shActive', 'toTD':True ,'launch':'checkTitles' ,'justVerify':False,'getSuggParam':True,'AStype':'title'},
    'checkPhones'  :{'readRange':'selection','toTD':False,'launch':'rangeChecker','justVerify':False,'getSuggParam':True,'AStype':'phone'},
    'checkEmails'  :{'readRange':'selection','toTD':False,'launch':'rangeChecker','justVerify':False,'getSuggParam':True,'AStype':'mail'},
    'checkWebsites':{'readRange':'selection','toTD':False,'launch':'rangeChecker','justVerify':False,'getSuggParam':True,'AStype':'website'}
    }

# readLib    : прочитать подходящие варианты для валидации из библиотеки
# checkList  : валидация путём проверки, есть ли value в списке допустимых (extra)
# acceptBlank: для диалога с предложением исправить (None означает, что надо прочитать из настроек)
# ↓ !ВСЕ ЭТИ ТИПЫ ДОЛЖНЫ БЫТЬ В strings.suggMsg! ↓
AStypes = {'title'  :{'readLib':True ,'checkList':True ,'acceptBlank':False},
           'phone'  :{'readLib':False,'checkList':False,'acceptBlank':None },
           'mail'   :{'readLib':False,'checkList':False,'acceptBlank':True },
           'website':{'readLib':False,'checkList':False,'acceptBlank':True }}

log = {'units' :{'mainLaunch'  :'core',
                 'launchType'  :'core', # отсутствует в S.log: читается из S.layout
                 'readSheet'   :'core',
                 'readFile'    :'core',
                 'ACsuccess'   :'autocorr',
                 'errorsFound' :'errors',
                 'suggFinished':'sugg',
                 'finalWrite'  :'core',
                 'colorErrors' :'core'},
       'colors':{'core'        : None,
                 'autocorr'    :'sand',
                 'errors'      :'red',
                 'sugg'        :'magenta'}}

# прочее
exBooks = exBooks()

# особые символы
# ↓ неподходящие для почты и сайта
badSymbols   = {'mail'   :(':','|','/','’',' ','<','>','[',']','.@','@.','@-.'),
                'website':(' ','@','|')}
badWebStarts = ('http://'  ,'https://'  ,'www.')
rmSites      = ('facebook.','instagram.','twitter.')

allHyphens   = ('-','–','—')
ruSymbols    = ('а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п',
                'р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я')

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
