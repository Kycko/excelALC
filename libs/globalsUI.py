from sys import exit as SYSEXIT

class globUI(): # импортируется в G.UI (в глобальные переменные)
    def __init__(self):
        # базовые переменные приложения
        self.app = {'version': 'v.101',
                    'name'   : 'excelALC',
                    'themes' :('flatly','superhero'),   # светлая и тёмная темы
                    'size'   :(1000, 600)}
        self.app   ['title'] = self.app['title']+' '+self.app['version']    # название главного окна

        self.bttns = {'run:sugg'    :{'cancel'    :{'style':'danger'   ,'side':'top'  ,'padx':0},
                                      'ok'        :{'style':'success'  ,'side':'top'  ,'padx':7}},
                      'run:finished':{'openErrors':{'style':'secondary','side':'right','padx':0},
                                      'exit'      :{'style':'success'  ,'side':'left' ,'padx':0}}}

        # настройки по типам задач (вкладка main/extra/script, цвет кнопки)
        self.tasks   = {'allChecks'    : {'type':'main' ,'style':'success'},
                        'reCalc'       : {'type':'main' ,'style':'warning'},
                        'checkTitles'  : {'type':'main' ,'style':'primary'},
                        'checkCities'  : {'type':'main' ,'style':'primary'},
                        'checkCat'     : {'type':'main' ,'style':'primary'},
                        'checkVert'    : {'type':'main' ,'style':'primary'},
                        'checkSources' : {'type':'main' ,'style':'primary'},
                        'checkPhones'  : {'type':'main' ,'style':'primary'},
                        'checkEmails'  : {'type':'main' ,'style':'primary'},
                        'checkWebsites': {'type':'main' ,'style':'primary'},
                        'rmEmptyRC'    : {'type':'extra','style':'primary'},
                        'capitalize'   : {'type':'extra','style':'primary'},
                        'checkDates'   : {'type':'extra','style':'primary'},
                        'fillBlanks'   : {'type':'extra','style':'primary'},
                        'formatSheet'  : {'type':'extra','style':'warning'}}

        # check/radio/entryList ("да/нет"/радиовыбор/выпадающий список со свободным вводом)
        self.taskCfg = {'shared:newSheet'       :'check',
                        'shared:suggestErrors'  :'check',
                        'shared:saveAfter'      :'check',
                        'phones:noBlanks'       :'check',
                        'titles:reorder'        :'check',
                        'vert:autocorr'         :'check',
                        'vert:onlyBlanks'       :'check',
                        'rmEmptyRC:rmTitled'    :'check',
                        'capitalize:selected'   :'radio',
                        'formatSheet:justRange' :'check',
                        'formatSheet:changeFont':'check',
                        'formatSheet:font'      :'entryList'}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
