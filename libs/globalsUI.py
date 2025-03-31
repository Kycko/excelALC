from sys import exit as SYSEXIT

class globUI(): # импортируется в G.UI (в глобальные переменные)
    def __init__(self):
        # базовые переменные приложения
        self.app = {'version':'v.106',
                    'name'   :'excelALC'}
        self.app   ['title'] = self.app['name']+' '+self.app['version'] # название главного окна

        # стили оформления (темы, шрифты и т. п.)
        self.themes = ( 'flatly','superhero')   # светлая/тёмная
        self.sizes  = ({'lbl':'100%','size':(1000,600)},
                       {'lbl':'125%','size':(1050,650)},
                       {'lbl':'150%','size':(1100,700)},
                       {'lbl':'175%','size':(1150,750)})
        self.fonts  =  {'iconBig':('Calibri',17)}   # только для label'ов (для кнопок всё сложнее)
        self.icons  =  {'theme'  :{'light':'🔆','dark':'🌙'}}

        # цвета (разные для светлой[0] и тёмной[1] тем
        # !ИСП. G.UI.colors (он перезаписывается при смене темы, в appUI.Window.setUItheme())
        self.themeColors = ({'blue'    :'#277CD4',   # ↓ светлая
                             'green'   :'#4AAC7F',
                             'magenta' :'#936BCC',
                             'pink'    :'#D22E9E',
                             'red'     :'#DE3923',
                             'lightRed':'#E36B4F',
                             'sand'    :'#D1A63E'},
                            {'blue'    :'#7BBCFF',   # ↓ тёмная
                             'green'   :'#8EE4BD',
                             'magenta' :'#C4ABE7',
                             'pink'    :'#FBA1DE',
                             'red'     :'#EF6C32',
                             'lightRed':'#E36F47',
                             'sand'    :'#FFE5A7'})  # аналог lightYellow

        # ВСЕ виджеты с их структурой и свойствами
        self.build = {
            'init'      :{'rules':('clean'),    # необязательный параметр (особые доп. правила)
                          'type' : 'fr',        # fr(ame)
                          'wxKey': 'fRoot',     # ключ для appUI.Window.wx {}, ОБЯЗАТЕЛЕН ДЛЯ ФРЕЙМОВ
                          'pack' :{'fill':'both','expand':True,'padx':10,'pady':10},
                          'stash':['inLeft']},  # виджеты, вложенные в этот (с tuple'ами будет ошибка)
            'inLeft'    :{'type' : 'fr',
                          'pack' :{'fill':'both','side':'left','padx': 5},
                          'stash':['inBottom']},
            'inBottom'  :{'type' : 'fr',
                          'pack' :{'fill':'x','side':'bottom','pady': 5},
                          'stash':['inCfg']},#,'btnCloseApp'
            'inCfg'     :{'type' : 'lfr',       # labelFrame
                          'title': 'inCfg:lfr',
                          'pack' :{'fill':'x','side':'left'},
                          'stash':['inCfgTheme']},
            'inCfgTheme':{'type' : 'fr',
                          'pack' :{'anchor':'w','pady':3},
                          'stash':['icSun','icMoon','cbTheme']},
            'icSun'     :{'type' : 'ic',        # ic(on)
                          'build':{'text':self.icons['theme']['light'], # для иконок создаём Label
                                   'font':self.fonts['iconBig']},
                          'pack' :{'side':'left','padx':4}},
            'icMoon'    :{'type' : 'ic',
                          'build':{'text':self.icons['theme']['dark'],
                                   'font':self.fonts['iconBig']},
                          'pack':{'side':'right','padx':0}},
            'cbTheme'   :{'type' : 'cb',                # checkButton
                          'var'  : 'main:darkTheme',    # variable для BooleanVar
                          'bst'  : 'round-toggle',      # свойство bootstyle
                          'tt'   : 'inCfg:ttTheme',     # toolTip
                          'pack' :{'expand':True}},

            'run'       :{'rules':('clean')}
            }

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
