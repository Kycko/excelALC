from   sys import exit as SYSEXIT
import dictFuncs       as dictF
import strings         as S

class globUI(): # импортируется в G.UI (в глобальные переменные)
  def __init__(self):
    def _getShared(type:str,upd={}):
      # функция, передающая в self.build одинаковые свойства для однотипных элементов
      dict = {'fRoot'     :{'rules'  :{'start':('clean')},
                            'type'   : 'fr',
                            'wxKey'  : 'fRoot',
                            'pack'   :{'fill':'both','expand':True,'padx':10,'pady':10}},
              'ilTab'     :{'rules'  :{'final':('packTab')},
                            'type'   : 'fr',
                            'pack'   :{'fill'   :'both'},
                            'packTab':{'padding': 7}},  # свойства для правила 'packTab'
              'scrollTab' :{'rules'  :{'final':('packTab')},
                            'type'   : 'sfr', # ScrollFrame
                            'pack'   :{'fill'   :'both'},
                            'packTab':{'padding': 7}},
              'il:taskBtn':{'type'   : 'btn',
                            'cmd'    :{'type' :'il:taskBtn'},
                            'build'  :{'width': 45},
                            'pack'   :{'pady' :  5}},
              'ir:tc:cb'  :{'rules'  :{'start':('mergeTC')},
                            'type'   : 'cb',
                            'build'  :{'bootstyle':'round-toggle'},
                            'pack'   :{'anchor'   :'nw',
                                       'expand'   : True,
                                       'padx'     : 5,
                                       'pady'     : 5}},
              'irFileLbl' :{'type'   : 'lbl',
                            'pack'   :{'anchor':'w','padx':5}},
              'log'       :{'rules'  :{'final':('paramsConfig')},
                            'type'   : 'lbl',
                            'pack'   :{'fill':'x'}}}
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
      # type     = fr(ame),lfr(labelFrame),cb(checkButton),tt(toolTip),tbs(tabs=TBS.Notebook),...
      # wxKey    = ключ для сохранения виджетов в памяти (в appUI.Window.wx{})
      # var/tVar = variable для BooleanVar, ОБЯЗАТЕЛЬНА для type = cb
      # cmd      = {type = тип для _bindCmd(), lmb = для lambda}
      # build    = свойства для создания самого виджета
      # pack     = параметры упаковки во фрейм
      # stash    = виджеты, вложенные в этот (исп. list[], т. к. с tuple'ами будет ошибка)

      # il,ir = initLeft,initRight
      # tc = task cfg
      # rl,rr,re,rb = runLog,runRight:[runErrors,runButtons]
      'init'           : _getShared('fRoot',{'root':{'stash':['il']}}),
      'il'             :{'type' : 'fr',
                         'pack' :{'fill':'both','side':'left','padx': 7},
                         'stash':['ilTabs','ilBottom']},
      'ilTabs'         :{'type' : 'tbs',
                         'pack' :{'fill':'both','expand':True,'pady':7},
                         'stash':['ilTabMain','ilTabSec']},
      'ilTabMain'      : _getShared('ilTab',
                                   {'inner':{'packTab':{'text':S.UI['ilTabMain']}},
                                    'root' :{'stash'  :['il:chkCat',  # chk = check
                                                        'il:chkSrc']}}),
      'ilTabSec'       : _getShared('ilTab',
                                   {'inner':{'packTab':{'text':S.UI['ilTabSec']}},
                                    'root' :{'stash'  :[]}}),
      'il:chkCat'      : _getShared('il:taskBtn',
                                   {'inner':{'cmd'  :{'lmb'      :'chkCat'},
                                             'build':{'text'     : S.UI['tasks']['chkCat']['ilBtn'],
                                                      'bootstyle':'primary'}}}),
      'il:chkSrc'      : _getShared('il:taskBtn',
                                   {'inner':{'cmd'  :{'lmb'      :'chkSrc'},
                                             'build':{'text'     : S.UI['tasks']['chkSrc']['ilBtn'],
                                                      'bootstyle':'primary'}}}),
      'ilBottom'       :{'type' : 'fr',
                         'pack' :{'fill':'x','side':'bottom','pady': 5},
                         'stash':['ilCfg','il:closeApp']},
      'ilCfg'          :{'type' : 'lfr',
                         'build':{'text':S.UI['ilCfg:lfr']},
                         'pack' :{'fill':'x','side':'left'},
                         'stash':['il:cfgTheme','il:cfgZoom']},
      'il:cfgTheme'    :{'type' : 'fr',
                         'pack' :{'pady':3},
                         'stash':['il:lblSun','il:lblMoon','il:cbTheme']},
      'il:lblSun'      :{'type' : 'lbl',
                         'build':{'text':self.icons['sun'],
                                  'font':self.fonts['iconBig']},
                         'pack' :{'side':'left','padx':4}},
      'il:lblMoon'     :{'type' : 'lbl',
                         'build':{'text':self.icons['moon'],
                                  'font':self.fonts['iconBig']},
                         'pack' :{'side':'right','padx':0}},
      'il:cbTheme'     :{'type' : 'cb',
                         'var'  : 'main:darkTheme',
                         'build':{'bootstyle':'round-toggle'},
                         'pack' :{'expand'   : True},
                         'stash':['il:ttTheme']},
      'il:ttTheme'     :{'type' : 'tt',
                         'build':{'text' :S.UI['ilCfg:ttTheme']}},
      'il:cfgZoom'     :{'rules':{'final':    ('build:zoomBtn')},
                         'type' : 'btn',
                         'wxKey': 'cfgZoom',
                         'cmd'  :{'type'     :'UIzoom'},
                         'build':{'bootstyle':'secondary'},
                         'pack' :{'padx':4   ,'pady':4}},
      'il:closeApp'    :{'type' : 'btn',
                         'cmd'  :{'type'     :        'closeApp'},
                         'build':{'text'     :S.UI['il:closeApp'],
                                  'width'    :  25,
                                  'bootstyle':  'danger'},
                         'pack' :{'side':'right','anchor':'s','padx':4,'pady':4}},

      'ir'             :{'rules':{'start':('saveProps'),'final':('build:ir')},
                         'type' : 'lfr',
                         'wxKey': 'ir',
                         'pack' :{'fill':'both','side':'right','expand':True,'padx':6},
                         'stash':['irDesc','irCfg','irBottom']},
      'irDesc'         :{'type' : 'lbl',
                         'wxKey': 'irDesc',
                         'build':{'wraplength':620},
                         'pack' :{'fill':'x','padx':8,'pady':5}},
      'irCfg'          :{'rules':{'final':('build:irCfg')},
                         'type' : 'fr',
                         'pack' :{'fill':'x','anchor':'nw','padx':8},
                         'stash':['irSep']},
      'irSep'          :{'type' : 'sep',
                         'pack' :{'fill':'x','padx':2,'pady':6}},
      'irBottom'       :{'rules':{'final':('build:irBottom')},
                         'type' : 'fr',
                         'pack' :{'fill':'x','side':'bottom','padx':22},
                         'stash':['ir:launchBtn','irFile']},
      'irFile'         :{'type' : 'fr',
                         'pack' :{'side':'left'},
                         'stash':['irFile:desc','irFile:upd']},
      'irFile:desc'    :{'type' : 'fr',
                         'pack' :{'side':'right'},
                         'stash':['irFile:file','irFile:sheet']},
      'irFile:file'    : _getShared('irFileLbl',{'root':{'wxKey':'irFile:file' }}),
      'irFile:sheet'   : _getShared('irFileLbl',{'root':{'wxKey':'irFile:sheet'}}),
      'irFile:upd'     :{'type' : 'btn',
                         'cmd'  :{'type'     :      'irFile:upd'},
                         'build':{'text'     : S.UI['irFile:upd'], # норм. иконку в конпке не сделать
                                  'bootstyle':'secondary'},
                         'pack' :{'side'     :'right',
                                  'fill'     :'both'}},
      'ir:launchBtn'   :{'type' : 'btn',
                         'wxKey': 'ir:launchBtn',
                         'cmd'  :{'type':'ir:launchBtn'},
                         'build':{'bootstyle':'success'},
                         'pack' :{'fill':'x','side':'bottom','pady':12}},

      'tc:newSheet'    : _getShared('ir:tc:cb',{'root':{'tVar':'newSheet'}}), # tVar = task var
      'tc:suggErrors'  : _getShared('ir:tc:cb',{'root':{'tVar':'suggErrors'}}),
      'tc:confirmWrite': _getShared('ir:tc:cb',{'root':{'tVar':'confirmWrite'}}),
      'tc:saveAfter'   : _getShared('ir:tc:cb',{'root':{'tVar':'saveAfter'}}),

      'run'            : _getShared('fRoot',{'root':{'stash':['rl','rr']}}),
      'rl'             :{'type' : 'fr',
                         'pack' :{'fill':'both','expand':True,'side':'left'},
                         'stash':['rlLbl','rlTabs']},
      'rr'             :{'type' : 'fr',
                         'pack' :{'fill':'both','expand':True,'side':'right','padx':5},
                         'stash':['rb','re']},
      'rlLbl'          :{'type' : 'lbl',
                         'build':{'text':S.UI['rl:lbl']},
                         'pack' :{'anchor':'w','padx':10}},
      'rlTabs'         :{'type' : 'tbs',
                         'pack' :{'fill':'both','expand':True,'padx':5,'pady':7},
                         'stash':['rlTabMain','rlTabErrors']},
      'rlTabMain'      : _getShared('scrollTab',
                                   {'inner':{'packTab':{'text':S.UI['rl:main']}},
                                    'root' :{'wxKey'  : 'rl:main'}}),
      'rlTabErrors'    : _getShared('scrollTab',
                                   {'inner':{'packTab':{'text':S.UI['rl:errors']}},
                                    'root' :{'wxKey'  : 'rl:errors'}}),
      'rb'             :{'type' : 'lfr',
                         'wxKey': 'rbLfr',
                         'build':{'text':S.UI['rb:init']},
                         'pack' :{'fill':'both','expand':True},
                         'stash':['rbRoot']},
      'rbRoot'         :{'type' : 'fr',
                         'wxKey': 'rbRoot',
                         'pack' :{'fill':'both','expand':True},
                         'stash':['rbe:cur']}, # e в rbe = errors (обработка ошибок)
      'rbe:cur'        :{'type' : 'fr',
                         'pack' :{'fill':'x','side':'top','padx':10,'pady':5},
                         'stash':['rbe:curLbl']},
      'rbe:curLbl'     :{'type' : 'lbl',
                         'build':{'text':S.UI['rbe:curLbl']},
                         'pack' :{'side':'left'}},
      're'             :{'type' : 'lfr',
                         'wxKey': 'errQueue',
                         'build':{'text' : S.UI['re:lfr']},
                         'pack' :{'fill' :'both','expand':True,'pady':7}},
      're:entry'       : _getShared('log',{'root':{'rules':{'final':('paramsConfig',
                                                                     'returnWidget')}}}),

      'log'            : _getShared('log'),
      }

    # цвета журнала (выбираются по юниту)
    self.log = {'core'      : None,
                'autocorr'  :'sand',
                'capitalize':'sand',
                'errors'    :'red',
                'rmRC'      :'pink',
                'warning'   :'red',
                'sugg'      :'magenta',
                'titles'    :'blue',
                'finalWrite':'green'}

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
