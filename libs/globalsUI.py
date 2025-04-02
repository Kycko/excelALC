from   sys import exit as SYSEXIT
import strings         as S

class globUI(): # импортируется в G.UI (в глобальные переменные)
    def __init__(self):
        # базовые переменные приложения
        self.app = {'version':'v.123',  'name':'excelALC'}
        self.app   ['title'] = self.app['name']+' '+self.app['version'] # название главного окна

        # стили оформления (темы, шрифты и т. п.)
        self.themes = ( 'flatly','superhero')   # светлая/тёмная
        self.sizes  = ({'lbl':'100%','size':(1000,600)},
                       {'lbl':'125%','size':(1050,650)},
                       {'lbl':'150%','size':(1100,700)},
                       {'lbl':'175%','size':(1150,750)})
        self.fonts  =  {'iconBig':('Calibri',17)}   # только для label'ов (для кнопок всё сложнее)
        self.icons  =  {'moon':'🌙','sun':'🔆'}

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
            # 'build' исп. при создании самого виджета, а 'pack' для упаковки во фрейм
            'init'       :{'sRules':('clean'),  # (s=start) особые правила В НАЧАЛЕ buildUI()
                           'type' : 'fr',       # fr(ame)
                           'wxKey': 'fRoot',    # ключ для сохранения виджетов в памяти (wx{})
                           'pack' :{'fill':'both','expand':True,'padx':10,'pady':10},
                           'stash':['inLeft']}, # виджеты, вложенные в этот (с tuple'ами будет ошибка)
            'inLeft'     :{'type' : 'fr',
                           'pack' :{'fill':'both','side':'left','padx': 5},
                           'stash':['inBottom']},
            'inBottom'   :{'type' : 'fr',
                           'pack' :{'fill':'x','side':'bottom','pady': 5},
                           'stash':['inCfg']},#,'btnCloseApp'
            'inCfg'      :{'type' : 'lfr',      # labelFrame
                           'build':{'text':S.UI['inCfg:lfr']},
                           'pack' :{'fill':'x','side':'left'},
                           'stash':['inCfgTheme','btnCfgZoom']},
            'inCfgTheme' :{'type' : 'fr',
                           'pack' :{'anchor':'w','pady':3},
                           'stash':['lblSun','lblMoon','cbTheme']},
            'lblSun'     :{'type' : 'lbl',      # label
                           'build':{'text':self.icons['sun'],
                                    'font':self.fonts['iconBig']},
                           'pack' :{'side':'left','padx':4}},
            'lblMoon'    :{'type' : 'lbl',
                           'build':{'text':self.icons['moon'],
                                    'font':self.fonts['iconBig']},
                           'pack':{'side':'right','padx':0}},
            'cbTheme'    :{'type' : 'cb',               # checkButton
                           'var'  : 'main:darkTheme',   # variable для BooleanVar
                           'build':{'bootstyle':'round-toggle'},
                           'pack' :{'expand'   : True},
                           'tt'   : 'inCfg:ttTheme'},   # toolTip
            'btnCfgZoom' :{'fRules':('buildZoomBtn'),   # (f=final) особые правила В КОНЦЕ buildUI()
                           'type' : 'btn',
                           'wxKey': 'btnCfgZoom',
                           'build':{'bootstyle':'secondary'},
                           'pack' :{'padx':4   ,'pady':4}},

            'run'       :{'sRules':('clean')}
            }

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
