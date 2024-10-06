from sys        import exit  as SYSEXIT
from globalVars import files as gFiles

# надписи элементов интерфейса
# labels, labelFrames(lfl), buttons, checkBoxes, toolTips
layout = {
    'main'      :{
        'lbl' :{'selectFile':'Файл:'},
        'btn' :{'closeApp'  :'❌ Закрыть программу',
                'launch'    :{'ready'       :'🚀 Запустить',
                              'notChosen'   :'Файл не выбран',
                              'fileNotFound':'Файл не найден. Вы его закрыли?',
                              'oneColumn'   :'В выделенном диапазоне должен быть только один столбец'}},
        'tabs':{'main'      :'основные',
                'extra'     :'доп. функции',
                'script'    :'по проектам'},
        'msg' :{
            'noFilesFound':'Не найдено открытых файлов Excel',
            'cantReadLib' :'Ошибка чтения файла "'+gFiles['lib']+'". Программа не может быть запущена.'
            },
        'tt'  :{'filesUpdate':'Обновить список открытых файлов.',
                'selectTheme':'Выбрать светлую/тёмную тему оформления.'}
        },
    'run'       :{
        'lfl'     :{'mainLog' :'  Журнал  ',
                    'sugg'    :'  Исправление ошибок  ',
                    'errors'  :'  Оставшиеся ошибки  ',
                    'finished':'  Выполнение завершено успешно  '},
        'suggUI'  :{# для диалога исправления ошибок
            'errorsLeft':{'one' :' (это последняя)',
                          'many':' (осталось $$2)'},
            'errType'   :'Вид ошибки:',
            'curValue'  :{'lbl':'Текущее значение: ',
                          'btn':'N/A'},
            'vars'      :'Варианты исправления:',
            'lblEntry'  :'Введите правильный вариант или нажмите "Отмена",\nчтобы исправить позже самостоятельно.',
            'buttons'   :{# именно в таком порядке для упаковки в фрейм
                'cancel':{'text':'Отмена','style':'danger' ,'padx':0},
                'ok'    :{'text':'OK'    ,'style':'success','padx':7}
                }
            },
        'finished':{
            'title'  :'Всего осталось ошибок: ',
            'buttons':{
                'openErrors':{'text':'Открыть файл с ошибками' ,'style':'secondary','side':'right'},
                'exit'      :{'text':'Вернуться в главное меню','style':'success'  ,'side':'left'}
                }
            }
        },
    'actions'   :{
        'allChecks'    :{
            'type' :'main',                       # main/script
            'btn'  :'🚀 Выполнить все проверки (пока не работает)',    # кнопка
            'lfl'  :'  🚀 Все проверки  ',        # labelFrame
            'log'  :'Запущены все проверки',      # запись в журнале выполнения программы
            # описание ↓
            'descr':'Поочерёдно запускает все проверки, необходимые для подготовки файла к загрузке.\n\nЭта функция может менять данные во всех ячейках.'
            },
        'checkTitles'  :{
            'type' :'main',
            'btn'  :'📊 Проверить столбцы',
            'lfl'  :'  📊 Проверка столбцов  ',
            'log'  :'Запущена проверка столбцов',
            'descr':'Проверяет названия столбцов на текущем листе:\n 1. Исправляет ошибочные;\n 2. Добавляет обязательные;\n 3. Выстраивает их по порядку.\n\nЭта функция перемещает столбцы вправо/влево, но меняет данные только в заголовках.'
            },
        'checkCities'  :{
            'type' :'main',
            'btn'  :'⛪ Проверить города/регионы',
            'lfl'  :'  ⛪ Проверка городов/регионов  ',
            'log'  :'Запущена проверка городов/регионов',
            'descr':'Проверяет правильность городов/регионов в выделенном диапазоне:\n • Для городов с уникальными названиями можно указывать их названия;\n • Если одно и то же название города есть в разных регионах, должен быть указан уникальный ID города.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkCat'     :{
            'type' :'main',
            'btn'  :'⛏ Проверить категории',
            'lfl'  :'  ⛏ Проверка категорий  ',
            'log'  :'Запущена проверка категорий',
            'descr':'Проверяет указанные категории в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkVert'    :{
            'type' :'main',
            'btn'  :'🌈 Проверить вертикали',
            'lfl'  :'  🌈 Проверка вертикалей  ',
            'log'  :'Запущена проверка вертикалей',
            'descr':'Ищет во всей таблице столбец "Категория" (он обязательно должен быть для правильной работы функции) и проверяет, соответствуют ли указанным категориям вертикали в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkSources' :{
            'type' :'main',
            'btn'  :'📜 Проверить источники',
            'lfl'  :'  📜 Проверка источников  ',
            'log'  :'Запущена проверка источников',
            'descr':'Проверяет указанные источники в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkPhones'  :{
            'type' :'main',
            'btn'  :'☎ Проверить телефоны',
            'lfl'  :'  ☎ Проверка телефонов  ',
            'log'  :'Запущена проверка телефонов',
            'descr':'Проверяет правильность номеров телефонов в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkEmails'  :{
            'type' :'main',
            'btn'  :'@ Проверить почты',
            'lfl'  :'  @ Проверка почт  ',
            'log'  :'Запущена проверка почт',
            'descr':'Проверяет правильность адресов почт в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkWebsites':{
            'type' :'main',
            'btn'  :'📰 Проверить сайты',
            'lfl'  :'  📰 Проверка сайтов  ',
            'log'  :'Запущена проверка сайтов',
            'descr':'Проверяет правильность адресов сайтов в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },

        'rmEmptyRC' :{
            'type'  :'extra',
            'btn'   :'▟  Удалить пустые строки и столбцы',
            'lfl'   :'  ▟  Удаление пустых строк и столбцов  ',
            'log'   :'Запущено удаление пустых строк и столбцов',
            'descr' :'Ищет на всём листе строки и столбцы, в которых не заполнена ни одна ячейка, и удаляет их.\n\nЭта функция может менять данные во всех ячейках.'
            },
        'capitalize':{
            'type'  :'extra',
            'btn'   :'[Аа Аа] Изменить прописные/строчные буквы',
            'lfl'   :'  [Аа Аа] Изменение прописных/строчных букв  ',
            'log'   :'Запущено изменение прописных/строчных букв',
            'descr' :'Меняет прописные/строчные буквы во всех ячейках выделенного диапазона в соответствии с шаблоном,\nвыбранным ниже.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkDates':{
            'type' :'extra',
            'btn'  :'📆 Проверить формат дат',
            'lfl'  :'  📆 Проверка дат  ',
            'log'  :'Запущена проверка дат',
            'descr':'Проверяет все даты в выделенном диапазоне и приводит их к формату 27.03.2026.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },

        'testScript'   :{
            'type' :'script',
            'btn'  :'Тестовый скрипт',
            'lfl'  :'  Запуск тестового скрипта  ',
            'log'  :'Запущен тестовый скрипт',
            'descr':''
            }
        },
    'actionsCfg':{  # настройки конкретных проверок
        'forAll':{
            'newSheet' :{
                'lbl'  :'  Создать новый лист, не менять исходные данные',
                'tt'   :'Если включить, в исходные данные не будет внесено никаких изменений, а результаты выполнения скрипта будут записаны на отдельный лист.'
                },
            'suggestErrors':{
                'lbl'  :'  Предлагать сразу исправлять ошибки',
                'tt'   :'Вне зависимости от этой настройки все ошибки будут записаны в файл '+gFiles['errors']+'. Включите опцию, если хотите сразу их исправлять.'
                },
            'saveAfter':{
                'lbl'  :'  Сохранить файл после выполнения',
                'tt'   :'После выполнения всех команд скрипта сохраняет файл (то же самое, что происходит, когда Вы нажимаете кнопку "Сохранить" в Excel).'
                }
            },
        'checkTitles'  :{
            'reorder'  :{
                'lbl'  :'  Расставить столбцы по порядку',
                'tt'   :'Если включить, столбцы будут расставлены в заданном порядке (регион, категория, вертикаль и т. д.), а все столбцы с неправильными названиями будут размещены в конце, справа.'
                }
            },
        'checkPhones'  :{
            'noBlanks' :{
                'lbl'  :'  Вписать в пустые ячейки телефон 79999999999',
                'tt'   :'Включите для проверки основного телефона (когда обязательно должен быть указан хоть какой-то телефон), выключите для дополнительных.'
                }
            },
        'rmEmptyRC'    :{
            'rmTitled' :{
                'lbl'  :'  Удалять пустые столбцы с непустым заголовком',
                'tt'   :'Вне зависимости от этой настройки будут удалены все строки и столбцы, в которых не заполнена ни одна ячейка. Включите, чтобы дополнительно удалить столбцы, в которых заполнена только ячейка в первой строке.'
                }
            },
        'capitalize'   :{
             'Aa_Aa'   :{'lbl':'  [Аа Аа] Сделать первые буквы каждого слова прописными, остальные строчными'},
             'Aa_aa'   :{'lbl':'  [Аа аа] Сделать первую букву прописной, остальные строчными'},
             'Aa_aA'   :{'lbl':'  [Аа аА] Сделать первую букву прописной, остальные не трогать'},
             'AA_AA'   :{'lbl':'  [АА АА] Сделать все буквы прописными'},
             'aa_aa'   :{'lbl':'  [аа аа] Сделать все буквы строчными'}
            }
        }
    }
layout['actionsCfg']['allChecks'] = layout['actionsCfg']['checkTitles']

# ↓ для диалогов с предложением исправить
# !ВСЕ ЭТИ ТИПЫ ДОЛЖНЫ БЫТЬ В globalVars.AStypes!
suggMsg = {'title'  :'название столбца',
           'region' :'город/регион',
           'cat'    :'категория',
           'source' :'источник',
           'phone'  :'телефон',
           'mail'   :'e-mail',
           'website':'сайт',
           'date'   :'формат даты'}

# записи в журнале
log = {
    'mainLaunch'     : '[$$1] Файл: $$2', # 1:время запуска, 2:имя проверяемого файла
    'readSheet'      :'Выбран лист: $$1',
    'readFile'       :{# $$1:адрес, $$2:кол-во столбцов, $$3:кол-во строк
        'full'       :'Прочитана вся таблица ($$1): $$2, 1 заголовок + $$3',
        'range'      :'Прочитан диапазон $$1: $$2, $$3'
        },

    'ACsuccess'      :'[$$1] "$$2" -> "$$3"',                       # 1:тип, 2:что, 3:на что
    'errorsFound'    :'[$$1] Осталось ошибок: $$2 шт.',             # 1:тип, 2:кол-во ошибок
    'suggFinished'   :{
        'cancelled'  :'[$$1] Отменено пользователем: "$$2"',        # 1:тип, 2:что
        'accepted'   :'[$$1] Исправлено вручную: "$$2" -> "$$3"'    # 1:тип, 2:что, 3:на что
        },

    'titlesReordered':'Столбцы расставлены по порядку',
    'columnAdded'    :'Добавлен столбец: $$1',                      # 1:название столбца
    'RCremoved'      :{
        'none'       :'Пустые строки/столбцы не найдены',
        'main'       :'Удалено пустых строк/столбцов: $$1/$$2'
        },

    'finalWrite'     :{
        'skip'       :'Изменений нет, запись в файл не требуется',
        'main'       :'Результат записан на $$1 лист',  # 1 заменяется на след. ключ sheet
        'sheet'      :('тот же','новый')
        },
    'colorErrors'    :{
        'skip'       :'Фоновые цвета ячеек сброшены, ошибки НЕ будут выделены красным (их > 500 шт.)',
        'done'       :'Фоновые цвета ячеек сброшены, ошибки выделены красным: $$1 шт.', # 1:кол-во ошибок
        '0'          :'Фоновые цвета ячеек сброшены'
        },
    'fileSaved'      :'Выполнено сохранение файла'
    }

# ошибки ввода для suggUI
errInput = {'title'  :{'notInList'   :'Отсутствует в списке допустимых'},
            'region' :{'notInList'   :'Отсутствует в списке допустимых'},
            'cat'    :{'notInList'   :'Отсутствует в списке допустимых'},
            'source' :{'notInList'   :'Отсутствует в списке допустимых'},
            'phone'  :{'firstSymb'   :'Первая цифра 7?',
                       'kazakh'      :'Казахстанский телефон',
                       'length'      :'В телефоне 11 символов?',
                       'secNines'    :'79999999999 в доп. телефонах',
                       'nines_inMany':'79999999999 не нужен?',
                       'listDoubles' :'В строке есть дубли'},
            'mail'   :{'badSymbols'  :'Есть пробел или спец. символ',
                       'dogCount'    :'В почте одна @?',
                       'dotDomain'   :'В домене нет точки',
                       'dotsDomain'  :'Двойные точки в домене',
                       'endDomain'   :'Домен .ru или .com?',
                       'hyphen'      :'Только дефис/тире перед @',
                       'ru'          :'В почте есть кириллица',
                       '$'           :'В почте есть $',
                       'listDoubles' :'В строке есть дубли'},
            'website':{'badSymbols'  :'Есть пробел или спец. символ',
                       'dot'         :'В сайте нет ни одной точки',
                       'endSlash'    :'Сайт заканчивается символом /',
                       'wwwHttp'     :'Сайт начинается на http(s)/www',
                       'rmSites'     :'Facebook/Instagram/Twitter',
                       'listDoubles' :'В строке есть дубли'},
            'date'   :{'format'      :'Формат даты: 27.03.2026'}}

# словарь разных окончаний слов
words_byCount = {'столбцы':{'1':'столбец','2-4':'столбца','many':'столбцов'},
                 'строки' :{'1':'строка' ,'2-4':'строки' ,'many':'строк'}}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
