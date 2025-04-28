from   sys import exit as SYSEXIT
import dictFuncs       as dictF
import strings         as S

class globUI(): # импортируется в G.UI (в глобальные переменные)
  def __init__(self):
    def getShared(type:str,upd={}):
      # функция, передающая в self.build одинаковые свойства для однотипных элементов
      dict = {'inTab'    :{'rules'  :{'final':('packTab')},
                           'type'   : 'fr',
                           'pack'   :{'fill'   :'x'},
                           'packTab':{'padding': 7}}, # свойства для правила 'packTab'
              'inTaskBtn':{'type'   : 'btn',
                           'cmd'    :{'type' :'inTaskBtn'},
                           'build'  :{'width': 45},
                           'pack'   :{'pady' :  5}}}
      return dictF.update(dict[type],**upd)

    # базовые переменные приложения
    self.app = {'version':'v.159',  'name':'excelALC'}
    self.app   ['title'] = self.app['name']+' '+self.app['version'] # название главного окна

    # стили оформления (темы, шрифты и т. п.)
    self.themes = ( 'flatly','superhero')  # светлая/тёмная
    self.sizes  = ({'lbl':'100%','size':(1000,600)},
                   {'lbl':'125%','size':(1050,650)},
                   {'lbl':'150%','size':(1100,700)},
                   {'lbl':'175%','size':(1150,750)})
    self.fonts  =  {'iconBig':('Calibri',17)} # только для label'ов (для кнопок всё сложнее)
    self.icons  =  {'moon':'🌙','sun':'🔆'}

    # цвета (разные для светлой[0] и тёмной[1] тем
    # !ИСП. G.UI.colors (он перезаписывается при смене темы, в appUI.Window.setUItheme())
    self.themeColors = ({'blue'    :'#277CD4',  # ↓ светлая
                         'green'   :'#4AAC7F',
                         'magenta' :'#936BCC',
                         'pink'    :'#D22E9E',
                         'red'     :'#DE3923',
                         'lightRed':'#E36B4F',
                         'sand'    :'#D1A63E'},
                        {'blue'    :'#7BBCFF',  # ↓ тёмная
                         'green'   :'#8EE4BD',
                         'magenta' :'#C4ABE7',
                         'pink'    :'#FBA1DE',
                         'red'     :'#EF6C32',
                         'lightRed':'#E36F47',
                         'sand'    :'#FFE5A7'}) # аналог lightYellow

    # ВСЕ виджеты с их структурой и свойствами
    self.build = {
      # rules{start:, особые правила В НАЧАЛЕ buildUI()
      #       final:, ––||––         В КОНЦЕ  buildUI()
      #       other:} ––||––  в разных местах buildUI(), НУЖНО ВСТРАИВАТЬ в основной код
      # type  = fr(ame),lfr(labelFrame),cb(checkButton),tt(toolTip),tbs(tabs=TBS.Notebook),...
      # wxKey = ключ для сохранения виджетов в памяти (в appUI.Window.wx{})
      # var   = variable для BooleanVar, ОБЯЗАТЕЛЬНА для type = cb
      # cmd   = {type = тип для _bindCmd(), lmb = для lambda}
      # build = свойства для создания самого виджета
      # pack  = параметры упаковки во фрейм
      # stash = виджеты, вложенные в этот (исп. list[], т. к. с tuple'ами будет ошибка)
      'init'       :{'rules':{'start':('clean')},
                     'type' : 'fr',
                     'wxKey': 'fRoot',
                     'pack' :{'fill':'both','expand':True,'padx':10,'pady':10},
                     'stash':['inLeft']},
      'inLeft'     :{'type' : 'fr',
                     'pack' :{'fill':'both','side':'left','padx': 7},
                     'stash':['inTabs','inBottom']},
      'inRight'    :{'rules':{'start':('saveProps'),'final':('buildInRight')},
                     'type' : 'lfr',
                     'wxKey': 'fInRight',
                     'pack' :{'fill':'both','side':'right','expand':True,'padx':6}},
      'inTabs'     :{'type' : 'tbs',
                     'pack' :{'fill':'both','expand':True,'pady':7},
                     'stash':['inTabMain','inTabSec']},
      'inTabMain'  :  getShared('inTab',
                               {'inner':{'packTab':{'text':S.UI['inTabMain']}},
                                'root' :{'stash'  :['inBtnChkCat',  # chk = check
                                                    'inBtnChkSrc']}}),
      'inTabSec'   :  getShared('inTab',
                               {'inner':{'packTab':{'text':S.UI['inTabSec']}},
                                'root' :{'stash'  :[]}}),
      'inBtnChkCat':  getShared('inTaskBtn',
                               {'inner':{'cmd'  :{'lmb'      :'checkCat'},
                                         'build':{'text'     : S.UI['tasks']['checkCat']['inBtn'],
                                                  'bootstyle':'primary'}}}),
      'inBtnChkSrc':  getShared('inTaskBtn',
                               {'inner':{'cmd'  :{'lmb'      :'checkSrc'},
                                         'build':{'text'     : S.UI['tasks']['checkSrc']['inBtn'],
                                                  'bootstyle':'primary'}}}),
      'inBottom'   :{'type' : 'fr',
                     'pack' :{'fill':'x','side':'bottom','pady': 5},
                     'stash':['inCfg','btnCloseApp']},
      'inCfg'      :{'type' : 'lfr',
                     'build':{'text':S.UI['inCfg:lfr']},
                     'pack' :{'fill':'x','side':'left'},
                     'stash':['inCfgTheme','btnCfgZoom']},
      'inCfgTheme' :{'type' : 'fr',
                     'pack' :{'pady':3},
                     'stash':['lblSun','lblMoon','cbTheme']},
      'lblSun'     :{'type' : 'lbl',
                     'build':{'text':self.icons['sun'],
                              'font':self.fonts['iconBig']},
                     'pack' :{'side':'left','padx':4}},
      'lblMoon'    :{'type' : 'lbl',
                     'build':{'text':self.icons['moon'],
                              'font':self.fonts['iconBig']},
                     'pack' :{'side':'right','padx':0}},
      'cbTheme'    :{'type' : 'cb',
                     'var'  : 'main:darkTheme',
                     'build':{'bootstyle':'round-toggle'},
                     'pack' :{'expand'   : True},
                     'stash':['ttTheme']},
      'ttTheme'    :{'type' : 'tt',
                     'build':{'text' :S.UI['inCfg:ttTheme']}},
      'btnCfgZoom' :{'rules':{'final':    ('buildZoomBtn')},
                     'type' : 'btn',
                     'wxKey': 'btnCfgZoom',
                     'cmd'  :{'type'     :'UIzoom'},
                     'build':{'bootstyle':'secondary'},
                     'pack' :{'padx':4   ,'pady':4}},
      'btnCloseApp':{'type' : 'btn',
                     'cmd'  :{'type'     :             'closeApp'},
                     'build':{'text'     :S.UI['init:btnCloseApp'],
                              'width'    :  25,
                              'bootstyle':  'danger'},
                     'pack' :{'side':'right','anchor':'s','padx':4,'pady':4}},

      'run'        :{'rules':{'start':('clean')}}
      }

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
