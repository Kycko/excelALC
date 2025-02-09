from sys        import exit  as SYSEXIT
from globalsMain import files as gFiles

# надписи элементов интерфейса
# labels, labelFrames(lfl), buttons, checkBoxes, toolTips
layout = {
    'main'   :{
        'lbl' :{'selectFile'  :'Файл:'},
        'btn' :{'closeApp'    :'❌ Закрыть программу',
                'launch'      :{'ready'     :'🚀 Запустить',
                                'notChosen' :'Файл не выбран',
                                'cantLaunch':'Файл не найден. Вы его закрыли?'}},
        'tabs':{'main'        :'основные',
                'extra'       :'доп. функции',
                'script'      :'по проектам'},
        'msg' :{'noFilesFound':'Не найдено открытых файлов Excel',
                'cantReadLib' :'Ошибка чтения файла "'+gFiles['lib']+'". Программа не может быть запущена.'},
        'tt'  :{'filesUpdate' :'Обновить список открытых файлов.',
                'selectTheme' :'Выбрать светлую/тёмную тему оформления.'}
        },
    'run'    :{
        'lfl'     :{'mainLog'  :'  Журнал  ',
                    'sugg'     :'  Исправление ошибок  ',
                    'errors'   :'  Оставшиеся ошибки  ',
                    'finished' :'  Выполнение завершено успешно  ',
                    'launchErr':'  Ошибка запуска  '},
        'suggUI'  :{# для диалога исправления ошибок
            'errorsLeft':{'one' :' (это последняя)',
                          'many':' (осталось $$2)'},
            'errType'   :'Вид ошибки:',
            'curValue'  :{'lbl':'Текущее значение: ',
                          'btn':'N/A'},
            'vars'      :'Варианты исправления:',
            'lblEntry'  :'Введите правильный вариант или нажмите "Отмена",\nчтобы исправить позже самостоятельно.',
            'buttons'   :{'cancel':'Отмена',    # именно в таком порядке для правильного pack()
                          'ok'    :'OK'}
            },
        'finished':{
            'title'  :'Всего осталось ошибок: ',
            'errors' :{'oneColumn'   :'Выделено больше одного столбца',
                       'noCatsColumn':'Столбец "Категория" не найден'},
            'buttons':{'openErrors'  :'Открыть файл с ошибками',
                       'exit'        :'Вернуться в главное меню'}
            }
        },
    'tasks'  :{
        'allChecks'    :{
            'btn'  :'🚀 Выполнить все проверки',    # текст кнопки
            'lfl'  :'  🚀 Все проверки  ',          # labelFrame
            'log'  :'Запущены все проверки',        # запись в журнале выполнения программы
            # описание ↓
            'descr':'Поочерёдно запускает все проверки, необходимые для подготовки файла к загрузке.\n\nЭта функция может менять данные во всех ячейках.'
            },
        'reCalc'       :{
            'btn'  :'[123] Посчитать кол-во ошибок и уникальных',
            'lfl'  :'  [123] Подсчёт ошибок и уникальных  ',
            'log'  :'Запущен подсчёт ошибочных и уникальных значений',
            'descr':'Считывает весь лист, распознаёт столбцы по их заголовкам, после чего поочерёдно проверяет все ячейки в каждом столбце и в итоге для каждого столбца показывает количество уникальных значений, а также ячеек с ошибками.\n\nЭта функция не изменяет данные в таблице, только в шапке над заголовками столбцов.'
            },
        'checkTitles'  :{
            'btn'  :'📊 Проверить столбцы',
            'lfl'  :'  📊 Проверка столбцов  ',
            'log'  :'Запущена проверка столбцов',
            'descr':'Проверяет названия столбцов на текущем листе:\n 1. Исправляет ошибочные;\n 2. Добавляет обязательные;\n 3. Выстраивает их по порядку.\n\nЭта функция перемещает столбцы вправо/влево, но меняет данные только в заголовках.'
            },
        'checkCities'  :{
            'btn'  :'⛪ Проверить города/регионы',
            'lfl'  :'  ⛪ Проверка городов/регионов  ',
            'log'  :'Запущена проверка городов/регионов',
            'descr':'Проверяет правильность городов/регионов в выделенном диапазоне:\n • Для городов с уникальными названиями можно указывать их названия;\n • Если одно и то же название города есть в разных регионах, должен быть указан уникальный ID города.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkCat'     :{
            'btn'  :'⛏ Проверить категории',
            'lfl'  :'  ⛏ Проверка категорий  ',
            'log'  :'Запущена проверка категорий',
            'descr':'Проверяет указанные категории в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkVert'    :{
            'btn'  :'🌈 Проверить вертикали',
            'lfl'  :'  🌈 Проверка вертикалей  ',
            'log'  :'Запущена проверка вертикалей',
            'descr':'Ищет во всей таблице столбец "Категория" (он обязательно должен быть для правильной работы функции) и проверяет, соответствуют ли указанным категориям вертикали в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkSources' :{
            'btn'  :'📜 Проверить источники',
            'lfl'  :'  📜 Проверка источников  ',
            'log'  :'Запущена проверка источников',
            'descr':'Проверяет указанные источники в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkPhones'  :{
            'btn'  :'☎ Проверить телефоны',
            'lfl'  :'  ☎ Проверка телефонов  ',
            'log'  :'Запущена проверка телефонов',
            'descr':'Проверяет правильность номеров телефонов в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkEmails'  :{
            'btn'  :'@ Проверить почты',
            'lfl'  :'  @ Проверка почт  ',
            'log'  :'Запущена проверка почт',
            'descr':'Проверяет правильность адресов почт в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkWebsites':{
            'btn'  :'📰 Проверить сайты',
            'lfl'  :'  📰 Проверка сайтов  ',
            'log'  :'Запущена проверка сайтов',
            'descr':'Проверяет правильность адресов сайтов в выделенном диапазоне.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },

        'rmEmptyRC'  :{
            'btn'    :'▟  Удалить пустые строки и столбцы',
            'lfl'    :'  ▟  Удаление пустых строк и столбцов  ',
            'log'    :'Запущено удаление пустых строк и столбцов',
            'descr'  :'Ищет на всём листе строки и столбцы, в которых не заполнена ни одна ячейка, и удаляет их.\n\nЭта функция может менять данные во всех ячейках.'
            },
        'capitalize' :{
            'btn'    :'[Аа Аа] Изменить прописные/строчные буквы',
            'lfl'    :'  [Аа Аа] Изменение прописных/строчных букв  ',
            'log'    :'Запущено изменение прописных/строчных букв',
            'descr'  :'Меняет прописные/строчные буквы во всех ячейках выделенного диапазона в соответствии с шаблоном,\nвыбранным ниже.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'checkDates' :{
            'btn'    :'📆 Проверить формат дат',
            'lfl'    :'  📆 Проверка дат  ',
            'log'    :'Запущена проверка дат',
            'descr'  :'Проверяет все даты в выделенном диапазоне и приводит их к формату 27.03.2026.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'fillBlanks' :{
            'btn'    :'[abc] Вписать строку в пустые ячейки диапазона',
            'lfl'    :'  [abc] Заполнение пустых ячеек диапазона  ',
            'log'    :'Запущено заполнение пустых ячеек диапазона',
            'descr'  :'Проверяет каждую ячейку выделенного диапазона и вписывает указанную строку только в пустые.\n\nЭта функция может менять данные только в выделенном диапазоне.'
            },
        'formatSheet':{
            'btn'    :'✨ Исправить форматирование (шрифт и т. п.)',
            'lfl'    :'  ✨ Форматирование  ',
            'log'    :'Запущено форматирование (изменение внешнего вида)',
            'descr'  :'Применяет все выбранные ниже настройки к выделенному диапазону или всему листу.'
            }
        },
    'taskCfg':{ # настройки конкретных проверок
        'shared:newSheet'       :{
            'lbl':'  Создать новый лист, не менять исходные данные',
            'tt' :  'Если включить, в исходные данные не будет внесено никаких изменений, а результаты выполнения скрипта будут записаны на отдельный лист.'
            },
        'shared:suggestErrors'  :{
            'lbl':'  Предлагать сразу исправлять ошибки',
            'tt' :  'Вне зависимости от этой настройки все ошибки будут записаны в файл '+gFiles['errors']+'. Включите опцию, если хотите сразу их исправлять.'
            },
        'shared:saveAfter'      :{
            'lbl':'  Сохранить файл после выполнения',
            'tt' :  'После выполнения всех команд скрипта сохраняет файл (то же самое, что происходит, когда Вы нажимаете кнопку "Сохранить" в Excel).'
            },
        'phones:noBlanks'       :{
            'lbl':'  Не оставлять пустых ячеек в столбце "Основной телефон"',
            'tt' :  'Если включить, вместо пустых ячеек в столбце основных телефонов будет вписан номер 79999999999.'
            },
        'titles:reorder'        :{
            'lbl':'  Расставить столбцы по порядку',
            'tt' :  'Если включить, столбцы будут расставлены в заданном порядке (регион, категория, вертикаль и т. д.), а все столбцы с неправильными названиями будут размещены в конце, справа.'
            },
        'vert:autocorr'         :{
            'lbl':'  Автоматически исправлять ошибки',
            'tt' :  'Выключите, чтобы только подсветить ошибки, но не исправлять их автоматически.'
            },
        'vert:onlyBlanks'       :{
            'lbl':'  Только в пустых ячейках',
            'tt' :  'Включите, чтобы добавить вертикали только в пустые ячейки выделенного диапазона, а остальные не изменять.'
            },
        'rmEmptyRC:rmTitled'    :{
            'lbl':'  Удалять пустые столбцы с непустым заголовком',
            'tt' :  'Вне зависимости от этой настройки будут удалены все строки и столбцы, в которых не заполнена ни одна ячейка. Включите, чтобы дополнительно удалить столбцы, в которых заполнена только ячейка в первой строке.'
            },
        'capitalize:selected'   :{
            'vars':{'Aa_Aa':'  [Аа Аа] Сделать первые буквы каждого слова прописными, остальные строчными',
                    'Aa_aa':'  [Аа аа] Сделать первую букву прописной, остальные строчными',
                    'Aa_aA':'  [Аа аА] Сделать первую букву прописной, остальные не трогать',
                    'AA_AA':'  [АА АА] Сделать все буквы прописными',
                    'aa_aa':'  [аа аа] Сделать все буквы строчными'}
            },
        'formatSheet:justRange' :{
            'lbl'   :'  Только для выделенного диапазона',
            'tt'    :  'Если выключить, форматирование будет применено ко всему листу.'
            },
        'formatSheet:changeFont':{
            'enable': ('font'), # ПЕРЕМЕСТИТЬ указываем для галочек, которые включают/выключают доп. настройки
            'lbl'   :'  Изменить шрифт  ',
            'tt'    :  'Включите, чтобы изменить шрифт на выбранный ниже.'
            },
        'formatSheet:font'      :{
            'lbl'   : 'Шрифт (можно вручную ввести любой другой)',
            'vars'  :('Arial',
                      'Calibri',
                      'Cambria',
                      'Candara',
                      'Corbel',
                      'Gadugi',
                      'Gill Sans MT',
                      'Tahoma',
                      'Times New Roman',
                      'Trebuchet MS',
                      'Verdana')
            }
        }
    }

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
