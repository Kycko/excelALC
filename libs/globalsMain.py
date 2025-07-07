from sys          import exit as SYSEXIT
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

# горячие клавиши
keys = {'enter':('<Key-Return>','<KP_Enter>'),
        'pages':('<Prior>'     ,'<Next>')}  # PgUp,PgDown

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
