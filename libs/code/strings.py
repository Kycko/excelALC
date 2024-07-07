from sys        import exit  as SYSEXIT
from globalVars import files as gFiles

# надписи элементов интерфейса
# labels, labelFrames(lfl), buttons, checkBoxes, toolTips
layout = {
    'main':{
        'lbl' :{'selectFile'  :'Файл:'},
        'btn' :{'closeApp'    :'Закрыть программу',
                'launch'      :{'ready'     :'Запустить',
                                'notChosen' :'Файл не выбран',
                                'cantLaunch':'Файл не найден. Вы его закрыли?'}},
        'tabs':{'main'        :'Основные проверки',
                'script'      :'Скрипты проектов'},
        'msg' :{'noFilesFound':'Не найдено открытых файлов Excel',
                'cantReadLib' :'Ошибка чтения файла "'+gFiles['lib']+'". Программа не может быть запущена.'},
        'tt'  :{'filesUpdate' :'Обновить список открытых файлов.',
                'selectTheme' :'Выбрать светлую/тёмную тему оформления.'}
        },
    'run' :{
        'lfl'   :{'mainLog':'  Журнал  ',
                  'sugg'   :'  Исправление ошибок  ',
                  'errors' :'  Оставшиеся ошибки  '},
        'suggUI':{ # для диалога исправления ошибок
            'title'   :'Введите правильный вариант или нажмите "Отмена", чтобы исправить позже.',
            'curValue':'Текущее значение: '
            }},
    'actions' :{
        'allChecks'  :{
            'type'   :'main',                      # main/script
            'btn'    :'Выполнить все проверки',    # кнопка
            'lfl'    :'  Все проверки  ',          # labelFrame
            'log'    :'Запущены все проверки.',     # запись в журнале выполнения программы
            # описание ↓
            'descr'  :'Поочерёдно запускает все проверки, необходимые для подготовки файла к загрузке.\n\nЭта функция может менять данные во всех ячейках.'},
        'checkTitles':{
            'type'   :'main',
            'btn'    :'Проверить столбцы',
            'lfl'    :'  Проверка столбцов  ',
            'log'    :'Запущена проверка столбцов.',
            'descr'  :'Проверяет названия столбцов на текущем листе:\n 1. Исправляет ошибочные;\n 2. Добавляет обязательные;\n 3. Выстраивает их по порядку.\n\nЭта функция перемещает столбцы вправо/влево, но меняет данные только в заголовках.'},
        'checkEmails':{
            'type'   :'main',
            'btn'    :'Проверить почты',
            'lfl'    :'  Проверка почт  ',
            'log'    :'Запущена проверка почт.',
            'descr'  :'Проверяет правильность адресов почт в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'},
        'testScript' :{
            'type'   :'script',
            'btn'    :'Тестовый скриппт',
            'lfl'    :'  Запуск тестового скрипта  ',
            'log'    :'Запущен тестовый скрипт.',
            'descr'  :''}},
    'actionsCfg':{  # настройки конкретных проверок
        'forAll':{
            'newSheet'     :{
                'lbl'      :'  Создать новый лист, не менять исходные данные',
                'tt'       :'Если включить, в исходные данные не будет внесено никаких изменений, а результаты выполнения скрипта будут записаны на отдельный лист.'},
            'suggestErrors':{
                'lbl'      :'  Предлагать сразу исправлять ошибки',
                'tt'       :'Вне зависимости от этой настройки все ошибки будут записаны в файл '+gFiles['errors']+'. Включите опцию, если хотите сразу их исправлять.'},
            'saveAfter'    :{
                'lbl'      :'  Сохранить файл после выполнения',
                'tt'       :'После выполнения всех команд скрипта сохраняет файл (то же самое, что происходит, когда Вы нажимаете кнопку "Сохранить" в Excel).'}
            },
        'checkTitles':{
            'reorderColumns':{'lbl':'  Расставить столбцы по порядку',
                              'tt' :'Если включить, столбцы будут расставлены в заданном порядке (регион, категория, вертикаль и т. д.), а все столбцы с неправильными названиями будут размещены в конце, справа.'}
            }
        }
    }
layout['actionsCfg']['allChecks'] = layout['actionsCfg']['checkTitles']

# ↓ для диалогов с предложением исправить
# !ВСЕ ЭТИ ТИПЫ ДОЛЖНЫ БЫТЬ В globalVars.AStypes!
suggMsg = {'title':{'title':'Неправильное название столбца','curValue':'Текущее значение'},
           'mail' :{'title':'Неправильная почта'           ,'curValue':'Текущее значение'}}

# записи в журнале
log = {'readSheet'  :'[core] Выбран лист: $$1',
       'readFile'   :{# $$1:адрес, $$2:кол-во столбцов, $$3:кол-во строк
                      'full' :'[core] Прочитана вся таблица ($$1): $$2, 1 заголовок + $$3',
                      'range':'[core] Прочитан диапазон $$1: $$2, $$3'},
       'ACsuccess'  :'[autocorr] [$$1] $$2 -> $$3',            # 1: тип, 2:что, 3: на что
       'errorsFound':  '[errors] [$$1] Требуется исправить вручную: $$2 шт.'}  # 1: тип, 2: кол-во ошибок

# словарь разных окончаний слов
words_byCount = {'столбцы':{'1':'столбец','2-4':'столбца','many':'столбцов'},
                 'строки' :{'1':'строка' ,'2-4':'строки' ,'many':'строк'}}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
