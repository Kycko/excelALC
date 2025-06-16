from   sys import exit as SYSEXIT
import dictFuncs       as dictF
import strings         as S

class globUI(): # импортируется в G.UI (в глобальные переменные)
  def __init__(self):
    def _getShared(type:str,upd={}):
      # функция, передающая в self.build одинаковые свойства для однотипных элементов
      dict = {'fRoot'      :{'rules'  :{'start':('clean'),'final':('bindLogs')},
                             'type'   : 'fr',
                             'wxKey'  : 'fRoot',
                             'pack'   :{'fill':'both','expand':True,'padx':10,'pady':10}},
              'ilTab'      :{'rules'  :{'final':('packTab')},
                             'type'   : 'fr',
                             'pack'   :{'fill'   :'both'},
                             'packTab':{'padding': 7}},  # свойства для правила 'packTab'
              'scrollTab'  :{'rules'  :{'final':('packTab')},
                             'type'   : 'sfr', # ScrollFrame
                             'pack'   :{'fill'   :'both'},
                             'packTab':{'padding': 7}},
              'il:taskBtn' :{'rules'  :{'start':('il:taskBtn')},
                             'type'   : 'btn',
                             'cmd'    :{'type' :'il:taskBtn'},
                             'build'  :{'width': 45,'bootstyle':'primary'},
                             'pack'   :{'pady' :  3}},
              'irFileLbl'  :{'type'   : 'lbl',
                             'pack'   :{'anchor':'w','padx':5}},
              'log'        :{'rules'  :{'final':('paramsConfig')},
                             'type'   : 'lbl',
                             'pack'   :{'fill':'x'}},
              'rbeOkCancel':{'type'   : 'btn',
                             'pack'   :{'side':'left'}},
              'ir:tc:cb'   :{'rules'  :{'start':('mergeTC')},
                             'type'   : 'cb',
                             'build'  :{'bootstyle':'round-toggle'},
                             'pack'   :{'anchor'   :'nw',
                                        'expand'   : True,
                                        'padx'     : 5,
                                        'pady'     : 5}},
              'ir:tc:ent'  :{'rules'  :{'final':('TCent')},
                             'type'   : 'fr',
                             'pack'   :{'fill' : 'x','padx':5,'pady':5}},
              'ir:tc:rad'  :{'rules'  :{'final':('TCrad')},
                             'type'   : 'fr',
                             'pack'   :{'fill' : 'x','padx':5,'pady':5}}}
      return dictF.update(dict[type],**upd)

    # базовые переменные приложения
    self.app = {'version':'v.222',  'name':'excelALC'}
    self.app   ['title'] = self.app['name']+' '+self.app['version'] # название главного окна

    # стили оформления (темы, шрифты и т. п.)
    self.themes = ( 'flatly','superhero')  # светлая/тёмная
    self.sizes  = ({'lbl':'100%','size':(1000,700)},
                   {'lbl':'125%','size':(1050,750)},
                   {'lbl':'150%','size':(1100,800)},
                   {'lbl':'175%','size':(1150,850)})
    self.fonts  =  {'iconBig':('Calibri',17)} # только для label'ов (для кнопок всё сложнее)
    self.icons  =  {'moon':'🌙','sun'   :'🔆',
                    'done':'✔' ,'cancel':'❌',
                    'back':'<<<','rejectAll':'❌'}

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
      # type     = fr(ame),lfr(labelFrame),cb(checkButton),ent(entry),tbs(tabs=TBS.Notebook),...
      # wxKey    = ключ для сохранения виджетов в памяти (в appUI.Window.wx{})
      # var/tVar = variable для BooleanVar, ОБЯЗАТЕЛЬНА для type = cb
      # cmd      = {type = тип для _bindCmd(), lmb = для lambda}
      # build    = свойства для создания самого виджета
      # pack     = параметры упаковки во фрейм
      # stash    = виджеты, вложенные в этот (исп. list[], т. к. с tuple'ами будет ошибка)

      # il,ir = initLeft,initRight
      # tc = task cfg
      # rl,rr,re,rb = runLog,runRight:[runErrors,runButtons]
      'init'           :_getShared('fRoot',{'root':{'stash':['il']}}),
      'il'             :{
        'type' : 'fr',
        'pack' :{'fill':'both','side':'left','padx':7},
        'stash':['ilTabs','ilBottom']
        },
      'ilTabs'         :{
        'rules':{'final':('setFocus')},
        'type' : 'tbs',
        'wxKey': 'ilTabs',  # нужен для биндов PgUp/PgDown
        'pack' :{'fill':'both','expand':True,'pady':7},
        'stash':['ilTabMain','ilTabSec']
        },
      'ilTabMain'      :_getShared(
        'ilTab',
        {'inner':{'packTab':{'text':S.UI['ilTabMain']}},
         'root' :{'stash'  :['il:reCalc',
                             'il:chkTitles',  # chk = check
                             'il:chkCat',
                             'il:chkVert',
                             'il:chkSrc',
                             'il:chkMails']}}
        ),
      'ilTabSec'       :_getShared(
        'ilTab',
        {'inner':{'packTab':{'text':S.UI['ilTabSec']}},
         'root' :{'stash'  :['il:rmRC',
                             'il:capitalize',
                             'il:fillBlanks',
                             'il:formatSheet']}}
        ),
      'il:reCalc'      :_getShared(
        'il:taskBtn',
        {'inner':{'build':{'bootstyle':'warning'}}}
        ),
      'il:chkTitles'   :_getShared('il:taskBtn'),
      'il:chkCat'      :_getShared('il:taskBtn'),
      'il:chkVert'     :_getShared('il:taskBtn'),
      'il:chkSrc'      :_getShared('il:taskBtn'),
      'il:chkMails'    :_getShared('il:taskBtn'),
      'il:rmRC'        :_getShared('il:taskBtn'),
      'il:capitalize'  :_getShared('il:taskBtn'),
      'il:fillBlanks'  :_getShared('il:taskBtn'),
      'il:formatSheet' :_getShared(
        'il:taskBtn',
        {'inner':{'build':{'bootstyle':'warning'}}}
        ),

      'ilBottom'       :{
        'type' : 'fr',
        'pack' :{'fill':'x','side':'bottom','pady':5},
        'stash':['ilCfg','il:closeApp']
        },
      'ilCfg'          :{
        'type' : 'lfr',
        'build':{'text':S.UI['ilCfg:lfr']},
        'pack' :{'fill':'x','side':'left'},
        'stash':['il:cfgTheme','il:cfgZoom']
        },
      'il:cfgTheme'    :{
        'type' : 'fr',
        'pack' :{'pady':3},
        'stash':['il:lblSun','il:lblMoon','il:cbTheme']
        },
      'il:lblSun'      :{
        'type' : 'lbl',
        'build':{'text':self.icons['sun'],
                 'font':self.fonts['iconBig']},
        'pack' :{'side':'left','padx':4}
        },
      'il:lblMoon'     :{
        'type' : 'lbl',
        'build':{'text':self.icons['moon'],
                 'font':self.fonts['iconBig']},
        'pack' :{'side':'right','padx':0}
        },
      'il:cbTheme'     :{
        'type' : 'cb',
        'var'  : 'main:darkTheme',
        'build':{'bootstyle':'round-toggle'},
        'pack' :{'expand'   : True},
        'stash':['il:ttTheme']
        },
      'il:ttTheme'     :{
        'type' : 'tt',
        'build':{'text':S.UI['ilCfg:ttTheme']}
        },
      'il:cfgZoom'     :{
        'rules':{'final':('build:zoomBtn')},
        'type' : 'btn',
        'wxKey': 'cfgZoom',
        'cmd'  :{'type'     :'UIzoom'},
        'build':{'bootstyle':'secondary'},
        'pack' :{'padx':4   ,'pady':4}
        },
      'il:closeApp'    :{
        'type' : 'btn',
        'cmd'  :{'type'     :        'closeApp'},
        'build':{'text'     :S.UI['il:closeApp'],
                 'width'    :  25,
                 'bootstyle':'danger'},
        'pack' :{'side':'right','anchor':'s','padx':4,'pady':4}
        },

      'ir'             :{
        'rules':{'start':('saveProps'),'final':('build:ir','bindLogs')},
        'type' : 'lfr',
        'wxKey': 'ir',
        'pack' :{'fill':'both','side':'right','expand':True,'padx':6},
        'stash':['irDesc','irCfg','irBottom']
        },
      'irDesc'         :{
        'type' : 'lbl',
        'wxKey': 'irDesc',
        'build':{'wraplength':620},
        'pack' :{'fill':'x','padx':8,'pady':5}
        },
      'irCfg'          :{
        'rules':{'final':('build:irCfg')},
        'type' : 'fr',
        'pack' :{'fill':'x','anchor':'nw','padx':8},
        'stash':['irSep']
        },
      'irSep'          :{
        'type': 'sep',
        'pack':{'fill':'x','padx':2,'pady':6}
        },
      'irBottom'       :{
        'rules':{'final':('build:irBottom')},
        'type' : 'fr',
        'pack' :{'fill':'x','side':'bottom','padx':22},
        'stash':['ir:launchBtn','irFile']
        },
      'irFile'         :{
        'type' : 'fr',
        'pack' :{'side':'left'},
        'stash':['irFile:desc','irFile:upd']
        },
      'irFile:desc'    :{
        'type' : 'fr',
        'pack' :{'side':'right'},
        'stash':['irFile:file','irFile:sheet']
        },
      'irFile:file'    :_getShared(
        'irFileLbl',
        {'root':{'wxKey':'irFile:file'}}
        ),
      'irFile:sheet'   :_getShared(
        'irFileLbl',
        {'root':{'wxKey':'irFile:sheet'}}
        ),
      'irFile:upd'     :{ # норм. иконку в конпке не сделать
        'type' : 'btn',
        'cmd'  :{'type':'irFile:upd'},
        'build':{'text': S.UI['irFile:upd'],'bootstyle':'secondary'},
        'pack' :{'side':'right','fill':'both'}
        },
      'ir:launchBtn'   :{
        'rules':{'final':('setFocus')},
        'type' : 'btn',
        'wxKey': 'ir:launchBtn',
        'cmd'  :{'type'     :'ir:launchBtn'},
        'build':{'bootstyle':'success'},
        'pack' :{'fill':'x' ,'side':'bottom','pady':12}
        },

      'tcEnt:lbl'      :{
        'rules':{'final':('paramsConfig')},
        'type' : 'lbl',
        'pack' :{'side':'left','padx':4}
        },
      'tcEnt:ent'      :{
        'rules':{'final':('fillEnt','returnWidget')},
        'type' : 'ent',
        'pack' :{'fill':'x'}
        },
      'tc:radEntry'    :{
        'rules':{'final':('tc:radio')},
        'type' : 'radEntry',
        'pack' :{'fill':'x','padx':4,'pady':3}
        },

      'tc:newSheet'    :_getShared('ir:tc:cb',{'root':{'tVar':'newSheet'}}),  # tVar = task var
      'tc:suggErrors'  :_getShared('ir:tc:cb',{'root':{'tVar':'suggErrors'}}),
      'tc:saveAfter'   :_getShared('ir:tc:cb',{'root':{'tVar':'saveAfter'}}),
      'tc:rmTitledCols':_getShared('ir:tc:cb',{'root':{'tVar':'rmTitledCols'}}),
      'tc:ACverts'     :_getShared('ir:tc:cb',{'root':{'tVar':'ACverts'}}),
      'tc:vertBlanks'  :_getShared('ir:tc:cb',{'root':{'tVar':'vertBlanks'}}),
      'tc:reorder'     :_getShared('ir:tc:cb',{'root':{'tVar':'reorder'}}),
      # ↓ в коде зашито self.wx['tcl:'+tVar]
      'tc:strFiller'   :_getShared('ir:tc:ent',{'root':{'tVar':'strFiller'}}),
      'tc:captMask'    :_getShared(
        'ir:tc:rad',
        {'root':{'tVar':['Aa_Aa','Aa_aa','Aa_aA','AA_AA','aa_aa']}}
        ),
      'tc:frmRange'    :_getShared('ir:tc:cb',{'root':{'tVar':'frmRange'}}),
      'tc:frmFont'     :_getShared('ir:tc:cb',{'root':{'tVar':'frmFont'}}),
      'tc:frmBIU'      :_getShared('ir:tc:cb',{'root':{'tVar':'frmBIU'}}),
      'tc:frmAlign'    :_getShared('ir:tc:cb',{'root':{'tVar':'frmAlign'}}),
      'tc:frmNewLines' :_getShared('ir:tc:cb',{'root':{'tVar':'frmNewLines'}}),
      'tc:frmBorders'  :_getShared('ir:tc:cb',{'root':{'tVar':'frmBorders'}}),
      'tc:frmBg'       :_getShared('ir:tc:cb',{'root':{'tVar':'frmBg'}}),
      'tc:frmFg'       :_getShared('ir:tc:cb',{'root':{'tVar':'frmFg'}}),

      'run'            :_getShared('fRoot'   ,{'root':{'stash':['rl','rr']}}),
      'rl'             :{
        'type' : 'fr',
        'pack' :{'fill' :'both','expand':True,'side':'left'},
        'stash':['rlLbl','rlTabs']
        },
      'rr'             :{
        'type' : 'fr',
        'pack' :{'fill':'y','side':'right','padx':5},
        'stash':['rb','re']
        },
      'rlLbl'          :{
        'type' : 'lbl',
        'build':{'text'  : S.UI['rl:lbl']},
        'pack' :{'anchor':'w','padx':10}
        },
      'rlTabs'         :{
        'type' : 'tbs',
        'wxKey': 'rlTabs',
        'pack' :{'fill':'both','expand':True,'padx':5,'pady':7},
        'stash':['rlTabMain'  ,'rlTabErrors']
        },
      'rlTabMain'      :_getShared(
        'scrollTab',
        {'inner':{'packTab':{'text':S.UI['rl:main']}},
         'root' :{'wxKey'  : 'rl:main'}}
        ),
      'rlTabErrors'    :_getShared(
        'scrollTab',
        {'inner':{'packTab':{'text':S.UI['rl:errors']}},
         'root' :{'wxKey'  : 'rl:errors'}}
        ),

      'rb'             :{
        'rules':{'final':('bind_rbCancel')},
        'type' : 'lfr',
        'wxKey': 'rbLfr',
        'build':{'text':S.UI['rb:init']},
        'pack' :{'fill':'both','expand':True},
        'stash':['rbRoot']
        },
      'rbRoot'         :{
        'type' : 'fr',
        'wxKey': 'rbRoot',
        'pack' :{'fill':'both','padx':10,'pady':2},
        'stash':['rbeEntry','rbe:sep','rbe:cur']  # e в rbe = errors (обработка ошибок)
        },
      'rbeEntry'       :{
        'type' : 'fr',
        'pack' :{'fill':'x'   ,'anchor':'n'},
        'stash':['rbeEntry:up','rbe:curType','rbeEntry:bottom','rbeEntry:errMsg']
        },
      'rbeEntry:up'    :{
        'type' : 'fr',
        'pack' :{'fill':'x','anchor':'n'},
        'stash':['rbeEntry:upLbl','rbeEntry:upBtns']
        },
      'rbeEntry:upLbl' :{
        'type' : 'lbl',
        'build':{'text': S.UI['rbeEntry:lbl']},
        'pack' :{'fill':'x','side':'left','padx':2}
        },
      'rbeEntry:upBtns':{
        'type' : 'fr',
        'pack' :{'side':'right'},
        'stash':['rbeEntry:upExit','rbeEntry:upCanc']
        },
      'rbeEntry:upExit':{
        'type' : 'btn',
        'cmd'  :{'type':'rbExit'},
        'build':{'text':self.icons['back'],'bootstyle':'danger-outline'},
        'pack' :{'side':'left','padx':2},
        'stash':['rbeExit:tt']
        },
      'rbeExit:tt'     :{
        'type' : 'tt',
        'build':{'text':S.UI['rbeExit:tt']}
        },
      'rbeEntry:upCanc':{
        'type' : 'btn',
        'cmd'  :{'type':'rbeEntry:upCanc'},
        'build':{'text': self.icons['rejectAll'],'bootstyle':'danger-outline'},
        'pack' :{'side':'right'},
        'stash':['rbeCanc:tt']
        },
      'rbeCanc:tt'     :{
        'type' : 'tt',
        'build':{'text':S.UI['rbeCanc:tt']}
        },
      'rbe:curType'    :{
        'rules':{'final':('color:lightRed')},
        'type' : 'lbl',
        'wxKey': 'rbe:curType',
        'pack' :{'fill':'x','padx':2}
        },
      'rbeEntry:bottom':{
        'type' : 'fr',
        'pack' :{'fill':'x'},
        'stash':['rbeEntry:entry','rbeEntry:ok','rbeEntry:cancel']
        },
      'rbeEntry:entry' :{
        'rules':{'final':('rbeEntry')},
        'type' : 'ent',
        'wxKey': 'rbeEntry',
        'pack' :{'fill':'x','expand':True,'side':'left','padx':4,'pady':7}
        },
      'rbeEntry:ok'    :_getShared(
        'rbeOkCancel',
        {'root':{'rules':{'final':('setFocus')},
                 'wxKey': 'rbeEntry:ok',
                 'cmd'  :{'type':'rbeEntry','lmb':'ok'},
                 'build':{'text': self.icons['done'],'bootstyle':'success'}}}
        ),
      'rbeEntry:cancel':_getShared(
        'rbeOkCancel',
        {'root':{'cmd'  :{'type':'rbeEntry','lmb':'cancel'},
                 'build':{'text': self.icons['cancel'],'bootstyle':'danger'}}}
        ),
      'rbeEntry:errMsg':{
        'rules':{'final':('color:lightRed')},
        'type' : 'lbl',
        'wxKey': 'rbe:errMsg',
        'pack' :{'fill':'x'  ,'padx':2}
        },
      'rbe:sep'        :{
        'type': 'sep',
        'pack':{'fill':'x','expand':True,'anchor':'n','padx':2,'pady':3}
        },
      'rbe:cur'        :{
        'type' : 'fr',
        'pack' :{'fill':'x','expand':True,'anchor':'n','pady':4},
        'stash':['rbe:curVal']
        },
      'rbe:curVal'     :{
        'type' : 'fr',
        'pack' :{'fill':'x'},
        'stash':['rbe:curLbl','rbe:curBtn']
        },
      'rbe:curLbl'     :{
        'type' : 'lbl',
        'build':{'text': S.UI['rbe:curLbl']},
        'pack' :{'side':'left'}
        },
      'rbe:curBtn'     :{
        'type' : 'btn',
        'wxKey': 'rbe:curBtn',
        'build':{'bootstyle':'warning-outline'},
        'pack' :{'fill':'x' ,'side':'right'}
        },
      'rbeVars'        :{
        'type' : 'fr',
        'wxKey': 'rbeVars',
        'pack' :{'fill':'x'  ,'expand':True,'anchor':'nw'},
        'stash':['rbeVarsLbl','rbeVars:inner']
        },
      'rbeVarsLbl'     :{
        'type' : 'lbl',
        'build':{'text': S.UI['rbeVarsLbl']},
        'pack' :{'fill':'x'}
        },
      'rbeVars:inner'  :{
        'rules':{'final':('addSuggList')},
        'type' : 'fr',
        'wxKey': 'rbeVars:inner',
        'pack' :{'fill':'x','pady':3}
        },
      'rbeVars:item'   :{
        'rules':{'final':('addSuggItem')},
        'type' : 'fr',
        'pack' :{'fill':'x','pady':2},
        'stash':['rbeVars:itemNum','rbeVars:itemBtn']
        },
      'rbeVars:itemNum':{
        'type' : 'lbl',
        'wxKey': 'rbev:num',  # нужен только для правила 'addSuggItem'
        'pack' :{'side':'left','padx':1}
        },
      'rbeVars:itemBtn':{
        'type' : 'btn',
        'wxKey': 'rbev:btn',  # нужен только для правила 'addSuggItem'
        'build':{'bootstyle':'info-outline'},
        'pack' :{'side':'right','fill':'x','expand':True,'padx':4}
        },
      'rbf'            :{
        'rules':{'final':('bindLogs')},
        'type' : 'fr',  # f в rbf = finish
        'pack' :{'fill':'both','padx':10,'pady':2},
        'stash':['rbfLbl','rbfBtns']
        },
      'rbfLbl'         :{
        'rules':{'final':('paramsConfig')},
        'wxKey': 'rbfLbl',
        'type' : 'lbl',
        'pack' :{'fill':'x','anchor':'w','padx':1,'pady':4}
        },
      'rbfBtns'        :{
        'type' : 'fr',
        'pack' :{'anchor' :'w','padx':3,'pady':7},
        'stash':['rbfExit','rbfShowLog','rbfShowErrors']
        },
      'rbfExit'        :{
        'rules':{'final':('setFocus')},
        'type' : 'btn',
        'wxKey': 'rbfExit',
        'cmd'  :{'type'      :'rbExit'},
        'build':{'text'      : self.icons['back']+S.UI['rbfExit'],
                 'bootstyle' :'success'},
        'pack' :{'anchor'    :'w','padx':2,'pady':3}
        },
      'rbfShowLog'     :{
        'rules':{'final':('rbfShowLog')},
        'type' : 'btn',
        'cmd'  :{'type':'rbfShowLog'},
        'build':{'text'     : S.UI['rbfShowLog'],
                 'bootstyle':'info-outline'},
        'pack' :{'anchor'   :'w','padx':2,'pady':3}
        },
      'rbfShowErrors'  :{
        'rules':{'final':('rbfShowErrors')},
        'type' : 'btn',
        'cmd'  :{'type':'rbfShowErrors'},
        'build':{'text'     : S.UI['rbfShowErrors'],
                 'bootstyle':'info-outline'},
        'pack' :{'anchor'   :'w','padx':2,'pady':3}
        },

      're'             :{
        'type' : 'lfr',
        'wxKey': 're',
        'pack' :{'fill':'both','expand':True,'pady':7},
        'stash':['reInner']
        },
      'reInner'        :{
        'type' : 'sfr',
        'wxKey': 'errQueue',
        'pack' :{'fill':'both','expand':True,'padx':8,'pady':6}
        },
      're:item'        :_getShared(
        'log',
        {'root' :{'rules':{'final':('paramsConfig','returnWidget')}}}
        ),

      'log'            :_getShared('log')
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
