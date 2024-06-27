from sys          import exit as SYSEXIT
from excelRW      import exBooks
from userSettings import userCfg

# базовые переменные приложения
app = {'version': 'v.033',
       'title'  : 'excelALC',
       'themes' : ('flatly', 'superhero'),              # светлая и тёмная темы
       'size'   : (707, 470)}                           # при необходимости добавим в другой переменной размеры диалоговых окон
app   ['TV']    = app['title'] + ' ' + app['version']   # название главного окна

# файлы
picsDir = 'libs/pics/'
files   = {'config'       : app['title'] + '.config',
           'log'          : app['title'] + '.log',
           'errors'       : app['title'] + '.errors'}
pics    = {'filesUpdate'  : picsDir      + 'filesUpdate.png',   # нельзя здесь создавать PhotoImage, т. к. нужен master-объект
           'themeSelector': {'light': {'pic' : picsDir + 'themeLight.png',
                                       'side': 'left',
                                       'padx': 4},
                             'dark' : {'pic' : picsDir + 'themeDark.png',
                                       'side': 'right',
                                       'padx': 0}}}

# параметры по типам скриптов
# getSuggParam = надо ли прочитать из userCfg настройку suggestErrors
# AStype (нужен не везде) = тип проверки для autocorr & suggest
launchTypes = {'allChecks'  : {'fullRange':True,  'toTD':True , 'launch':'allChecks'   , 'getSuggParam':True},
               'checkTitles': {'fullRange':True,  'toTD':True , 'launch':'checkTitles' , 'getSuggParam':True, 'AStype':'title'},
               'checkPhones': {'fullRange':False, 'toTD':False, 'launch':'rangeChecker', 'getSuggParam':True, 'AStype':'phone'},
               'checkEmails': {'fullRange':False, 'toTD':False, 'launch':'rangeChecker', 'getSuggParam':True, 'AStype':'mail'}}
# ↓ ПОТОМ СВЕРИТЬ, ЗДЕСЬ ДОЛЖНЫ БЫТЬ ВСЕ НУЖНЫЕ ТИПЫ ↓
AStypes = {'title': {'readLib'  : True,   # список подходящих вариантов будет прочитан из библиотеки
                     'checkList': True,   # валидация путём проверки, есть ли value в списке допустимых (extra)
                     'suggMsg'  : {'acceptBlank':False, 'gend':'neutral'}}, # для диалога с предложением исправить
           'mail' : {'readLib'  : False,
                     'checkList': False,
                     'suggMsg'  : {'acceptBlank':True,  'gend':'female'}}}

# прочее
config    = userCfg(files['config'])
exBooks   = exBooks()

# особые символы
allHyphens = ('-','–','—')
ruSymbols  = ('а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я')

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
