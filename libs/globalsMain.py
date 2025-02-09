from sys          import exit as SYSEXIT
from userSettings import userCfg
from globalsUI    import globUI

# глобальные переменные интерфейса (UI)
UI = globUI()

# файлы
files = {'lib'   :    'справочник excelALC.xlsx',
         'config':UI.app['title']+       '.config',
         'log'   :UI.app['title']+  ' main.log',
         'errors':UI.app['title']+' errors.log'}

# настройки
config = userCfg(files['config'])

# особые символы и списки
initRegList = ['Россия','все регионы','другие регионы','другой регион']

# main region/city trims (только начало/конец строки)
# ЦИФРЫ НЕ ДОБАВЛЯТЬ! (будут ошибки типа "МСК+2" -> "Москва")
mrcTrims = (' ','.',',','(',')','/','|','\\','?','!','+','-','–','—')

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
