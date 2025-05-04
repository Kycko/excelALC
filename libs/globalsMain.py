from sys          import exit as SYSEXIT
from excelRW      import exBooks
from userSettings import userCfg
from globalsUI    import globUI
from globalsDict  import globDicts

# разное
UI   = globUI   ()  # глобальные переменные интерфейса (UI)
dict = globDicts()  # прочее (всякие списки с текстовыми данными)

# файлы
files = {'lib'   :'справочник excelALC.xlsx',
         'config': UI.app['name'] +  '.config',
         'log'   :    'main.log',
         'errors':  'errors.log'}

# настройки
config = userCfg(files['config'])

# прочее
exBooks = exBooks()

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
