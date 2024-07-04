from sys          import exit as SYSEXIT
from userSettings import userCfg

# базовые переменные приложения
app = {'version': 'v.050',
       'title'  : 'excelALC',
       'themes' : ('flatly', 'superhero'),          # светлая и тёмная темы
       'size'   : (1000, 600)}                      # при необходимости добавим в другой переменной размеры диалоговых окон
app   ['TV']    = app['title']+' '+app['version']   # название главного окна

# файлы
picsDir = 'libs/pics/'
files   = {'config'       : app['title']+'.config',
           'log'          : app['title']+'.log',
           'errors'       : app['title']+'.errors'}
pics    = {'filesUpdate'  : picsDir     +'filesUpdate.png',   # нельзя здесь создавать PhotoImage, т. к. нужен master-объект
           'themeSelector': {'light': {'pic' : picsDir+'themeLight.png',
                                       'side': 'left',
                                       'padx': 4},
                             'dark' : {'pic' : picsDir+'themeDark.png',
                                       'side': 'right',
                                       'padx': 0}}}

# прочее
config = userCfg(files['config'])

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
