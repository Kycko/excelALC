from sys        import exit  as SYSEXIT
from globalVars import files as gFiles

# надписи элементов интерфейса
# labels, labelFrames(lfl), buttons, checkBoxes, toolTips
layout = {
    'main'      :{
        'lbl' :{'selectFile':'Файл:'},
        'btn' :{'closeApp'  :'❌ Закрыть программу',
                'launch'    :{'ready'     :'🚀 Запустить',
                              'notChosen' :'Файл не выбран',
                              'cantLaunch':'Файл не найден. Вы его закрыли?'}},
        'tabs':{'main'      :'Основные проверки',
                'script'    :'Скрипты проектов'},
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
            'newSheet':{
                'lbl':'  Создать новый лист, не менять исходные данные',
                'tt' :'Если включить, в исходные данные не будет внесено никаких изменений, а результаты выполнения скрипта будут записаны на отдельный лист.'
                },
            'suggestErrors':{
                'lbl':'  Предлагать сразу исправлять ошибки',
                'tt' :'Вне зависимости от этой настройки все ошибки будут записаны в файл '+gFiles['errors']+'. Включите опцию, если хотите сразу их исправлять.'
                },
            'saveAfter':{
                'lbl':'  Сохранить файл после выполнения',
                'tt' :'После выполнения всех команд скрипта сохраняет файл (то же самое, что происходит, когда Вы нажимаете кнопку "Сохранить" в Excel).'
                }
            },
        'checkTitles' :{
            'reorder' :{
                'lbl' :'  Расставить столбцы по порядку',
                'tt'  :'Если включить, столбцы будут расставлены в заданном порядке (регион, категория, вертикаль и т. д.), а все столбцы с неправильными названиями будут размещены в конце, справа.'
                }
            },
        'checkPhones' :{
            'noBlanks':{
                'lbl' :'  Вписать в пустые ячейки телефон 79999999999',
                'tt'  :'Включите для проверки основного телефона (когда обязательно должен быть указан хоть какой-то телефон), выключите для дополнительных.'
                }
            }
        }
    }
layout['actionsCfg']['allChecks'] = layout['actionsCfg']['checkTitles']

# ↓ для диалогов с предложением исправить
# !ВСЕ ЭТИ ТИПЫ ДОЛЖНЫ БЫТЬ В globalVars.AStypes!
suggMsg = {'title'  :'название столбца',
           'region' :'город/регион',
           'phone'  :'телефон',
           'mail'   :'e-mail',
           'website':'сайт'}

# записи в журнале
log = {
    'mainLaunch'   : '[$$1] Файл: $$2', # 1:время запуска, 2:имя проверяемого файла
    'readSheet'    :'Выбран лист: $$1',
    'readFile'     :{# $$1:адрес, $$2:кол-во столбцов, $$3:кол-во строк
        'full'     :'Прочитана вся таблица ($$1): $$2, 1 заголовок + $$3',
        'range'    :'Прочитан диапазон $$1: $$2, $$3'
        },

    'ACsuccess'    :'[$$1] "$$2" -> "$$3"',                     # 1:тип, 2:что, 3:на что
    'errorsFound'  :'[$$1] Осталось ошибок: $$2 шт.',           # 1:тип, 2:кол-во ошибок
    'suggFinished' :{
        'cancelled':'[$$1] Отменено пользователем: "$$2"',      # 1:тип, 2:что
        'accepted' :'[$$1] Исправлено вручную: "$$2" -> "$$3"'  # 1:тип, 2:что, 3:на что
        },

    'finalWrite'   :{
        'skip'     :'Ошибок не было найдено, запись в файл не требуется',
        'main'     :'Результат записан на $$1 лист',    # 1 заменяется на след. ключ sheet
        'sheet'    :('тот же','новый')
        },
    'colorErrors'  :{
        'skip'     :'Фоновые цвета ячеек сброшены, ошибки НЕ будут выделены красным (их > 500 шт.)',
        'done'     :'Фоновые цвета ячеек сброшены, ошибки выделены красным: $$1 шт.',   # 1:кол-во ошибок
        '0'        :'Фоновые цвета ячеек НЕ сброшены, ошибок не осталось'
        },
    'fileSaved'    :'Выполнено сохранение файла'
    }

# ошибки ввода для suggUI
errInput = {'title'  :{'notInList'   :'Отсутствует в списке допустимых'},
            'region' :{'notInList'   :'Отсутствует в списке допустимых'},
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
                       'listDoubles' :'В строке есть дубли'},
            'website':{'badSymbols'  :'Есть пробел или спец. символ',
                       'dot'         :'В сайте нет ни одной точки',
                       'endSlash'    :'Сайт заканчивается символом /',
                       'wwwHttp'     :'Сайт начинается на http(s)/www',
                       'rmSites'     :'Facebook/Instagram/Twitter',
                       'listDoubles' :'В строке есть дубли'}}

# словарь разных окончаний слов
words_byCount = {'столбцы':{'1':'столбец','2-4':'столбца','many':'столбцов'},
                 'строки' :{'1':'строка' ,'2-4':'строки' ,'many':'строк'}}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
