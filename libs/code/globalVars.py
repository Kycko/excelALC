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
launchTypes  = {'allChecks'  : {'fullRange': True,  'toTD': True},
                'checkTitles': {'fullRange': True,  'toTD': True},
                'checkEmails': {'fullRange': False, 'toTD': False}}

# прочее
config  = userCfg(files['config'])
exBooks = exBooks()

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
