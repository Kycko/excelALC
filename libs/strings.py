from sys import exit as SYSEXIT

# надписи элементов интерфейса
# labels, labelFrames(lfr), buttons, checkBoxes, toolTips
UI = {'init:cantReadLib':'Ошибка чтения файла "$FILE$". Программа не может быть запущена.',
      'init:btnCloseApp':'❌ Закрыть программу',
      'inCfg:lfr'       : '  Настройки  ',
      'inCfg:zoomBtn'   :   'Масштаб: ',
      'inCfg:ttTheme'   :   'Выбрать светлую/тёмную тему оформления.',
      'inTabMain'       :   'основные',
      'inTabSec'        :   'доп. функции',
      
      'tasks':{
          'checkCat' :{
              'inBtn':  '⛏ Проверить категории',
              'inLfr':'  ⛏ Проверка категорий  ',
              'log'  :'Запущена проверка категорий',
              'descr':'Проверяет указанные категории в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'}}}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
