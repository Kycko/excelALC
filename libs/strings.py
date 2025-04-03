from sys import exit as SYSEXIT

# надписи элементов интерфейса
# labels, labelFrames(lfr), buttons, checkBoxes, toolTips
UI = {'init:cantReadLib':'Ошибка чтения файла "$FILE$". Программа не может быть запущена.',
      'init:btnCloseApp':'❌ Закрыть программу',
      'inCfg:lfr'       : '  Настройки  ',
      'inCfg:zoomBtn'   :   'Масштаб: ',
      'inCfg:ttTheme'   :   'Выбрать светлую/тёмную тему оформления.'}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
