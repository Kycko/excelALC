from sys       import exit as SYSEXIT
from globalsUI import globUI

# глобальные переменные интерфейса (UI)
UI = globUI()

# файлы
files = {'lib'   :'справочник excelALC.xlsx',
         'config': UI.app['name'] +  '.config',
         'log'   :    'main.log',
         'errors':  'errors.log'}

# прочее (всякие списки с текстовыми данными)
dict = 

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
