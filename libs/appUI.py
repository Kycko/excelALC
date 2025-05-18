from   sys                          import exit as SYSEXIT
from   os                           import startfile
from   tkinter                      import BooleanVar
import ttkbootstrap                     as TBS
from   ttkbootstrap.tooltip         import ToolTip
from   ttkbootstrap.dialogs.dialogs import Messagebox
import globalsMain                      as G
import strings                          as S
from   stringFuncs                  import replaceVars
from   globalFuncs                  import sysExit
from   excelRW                      import getCurExcel

def cantReadLib():
  Messagebox.ok(S.UI['init:cantReadLib'].replace('$file$',G.files['lib']),
                G.UI.app['title'])

class ScrollFrame(TBS.Frame):
  def  __init__(self,parent):
    def _bind():
      def _onFrameConfigure (e): cObj.    config  (scrollregion=cObj.bbox('all'))
      def _onCanvasConfigure(e): cObj.itemconfig  (cWin,  width=e.width)
      def _onMouseWheel     (e): cObj.yview_scroll(int(-1* (e.delta/120)),'units')
      def _onEnter          (e): cObj.  bind_all  ('<MouseWheel>',_onMouseWheel)
      def _onLeave          (e): cObj.unbind_all  ('<MouseWheel>')

      self.frame.bind('<Configure>',_onFrameConfigure)
      cObj .bind('<Configure>',_onCanvasConfigure)
      self.frame.bind('<Enter>',_onEnter)
      self.frame.bind('<Leave>',_onLeave)
      _onFrameConfigure(None)

    super().__init__(parent)
    cObj       = TBS.Canvas   (self)
    self.frame = TBS.Frame    (cObj)  # надо запомнить для wxKey и stash
    scroll     = TBS.Scrollbar(self,orient='vertical',command=cObj.yview)
    cObj.config               (yscrollcommand=scroll.set)

    scroll.pack(side='right',fill='y')
    cObj  .pack(side='left' ,fill='both',expand=True)
    cWin = cObj.create_window((4,4),window=self.frame,anchor='nw')
    _bind()
class Window     (TBS.Window):  # окно программы
  # конструкторы интерфейса
  def __init__     (self,app):
    def _bindSpace():
      def _call(event):
        try:
          widget = self.nametowidget(event.widget)
          widget.invoke()
        except KeyError: self.tk.call(event.widget,'invoke')
      self.bind_class('TButton','<Key-space>',_call,add='+')

    self.app = app  # для вызова функций класса Root() при нажатии кнопок
    super().__init__(title = G.UI.app['title'])
    self.setUItheme (G.config.get('main:darkTheme'))
    _bindSpace   ()
    self.buildUI ('init',self)
    self.place_window_center()  # расположить в центре экрана
  def getAllChilds (self,widget): # возвращает все вложенные виджеты, КРОМЕ Entry
    def _append(widget):
      if not isinstance(widget,TBS.Entry): final.append(widget)
    final = []
    for child in widget.winfo_children():
      if      len(child.winfo_children()) == 0: _append(child)
      else:
        _append     (widget)
        final.extend(self.getAllChilds(child))
    return final
  def buildUI      (self,key:str,parent,params=None):
    # key = build key (из G.UI.build{})
    # в params передаём любые доп. данные (напр., тип задачи для фрейма 'ir')
    # создание интерфейса
    def _startRules  ():
      try:
        rules = pr['rules']['start']
        if 'clean'     in rules:
          self.destroyWidget('fRoot')
          self.props = {} # properties, что нужно запоминать для обработки UI
          self.wx    = {} # здесь все ссылки на виджеты, которые надо хранить в памяти
        if 'saveProps' in rules: self.props.update(params)
        if 'mergeTC'   in rules:
          pr['var'] = self.props['curTask']+':'+pr['tVar']
          strings   = S.UI['tc'][pr['tVar']]
          newKey    = 'tc:tt:' + pr['tVar']
          pr['build']['text']  = strings['lbl']
          pr['stash']          = [newKey]
          G.UI.build [newKey]  = {'type':'tt','build':{'text':strings['tt']}}
      except: pass  # так проще, чем с доп. условиями
    def _finalRules  ():
      def _suggClicked(item:str): self.suggVarClicked(item)
      try:
        rules = pr['rules']['final']
        if 'packTab'        in rules: parent.add(widget,**pr['packTab'])
        if 'build:zoomBtn'  in rules: _setUIzoom()
        if 'build:ir'       in rules:
          tOp = S.UI['tasks'][self.props['curTask']]
          for widg in ('ir','irDesc'): self.wx[widg].config(text=tOp[widg])
        if 'build:irCfg'    in rules:
          for cKey in G.dict.tasks[self.props['curTask']]['cfg']:
            self.buildUI('tc:'+cKey,widget)
        if 'build:irBottom' in rules: _updFile()
        if 'paramsConfig'   in rules: widget.config(**params)
        if 'color:lightRed' in rules: widget.config(foreground=G.UI.colors['lightRed'])
        if 'bindLogs'       in rules:
          tabs = self.wx['rlTabs']
          for w in self.getAllChilds(self.wx['fRoot']):
            for kk in G.keys['pages']:
              w.bind(kk,lambda s:tabs.select(abs(tabs.index(tabs.select())-1)))
        if 'addSuggList'    in rules:
          for i in range(len(params)): self.buildUI('rbeVars:item',
                                                    widget,
                                                    {'num':i+1,'item':params[i]})
        if 'addSuggItem'    in rules:
          p   = params
          num = p['num'] if p['num'] < 10 else 0
          self.wx['rbev:num'].config(text        = num)
          self.wx['rbev:btn'].config(text        = p['item']['btn'],
                                     command     = lambda  :_suggClicked(p['item']['val']))
          for w in self.getAllChilds(self.wx['fRoot']):
            w.bind(num,lambda s:_suggClicked(p['item']['val']))
        if 'rbeEntry'       in rules:
          for key in G.keys['enter']:
            self.wx['rbeEntry'].bind(key,
                                     lambda _:_suggFinalClicked('ok'))  # без _ ошибка
        if 'setFocus'       in rules: widget.focus_set()
        if 'returnWidget'   in rules: return widget
      except: pass  # так проще, чем с доп. условиями
    def _createWidget():
      bld = pr['build'] if 'build' in pr.keys() else {}
      match pr['type']:
        case 'btn': return TBS.     Button(parent,**bld)
        case 'cb' : return TBS.Checkbutton(
          parent,
          variable = BooleanVar(value=G.config.get(pr['var'])),
          **bld
          )
        case 'ent': return TBS.Entry      (parent)
        case  'fr': return TBS.Frame      (parent)
        case 'lbl': return TBS.Label      (parent,**bld)
        case 'lfr': return TBS.Labelframe (parent,**bld)
        case 'sep': return TBS.Separator  (parent)
        case 'sfr': return     ScrollFrame(parent)
        case 'tbs': return TBS.Notebook   (parent)
        case 'tt' : return     ToolTip    (parent,**bld)
    # изменение оформления
    def _setUIzoom(change=False):
      cfgName = 'main:zoom'
      sList   =  G.UI.sizes
      cur     =  G.config.get(cfgName)
      if change:
        cur += 1
        if cur == len(sList): cur = 0
        G .config.set(cfgName,cur)

      self.wx['cfgZoom'].config(text = S.UI['ilCfg:zoomBtn']+sList[cur]['lbl'])
      x,y = sList[cur]['size']
      self.geometry(str(x)+'x'+str(y))
      self.minsize (x,y)
    # кнопки и переключатели
    def _bindCmd():
      # w = widget; key,pr = ключ и свойства из G.UI.build{}
      match pr['type']:
        case 'cb' : widget.config(command=lambda:_switchBoolSetting(pr['var']))
        case 'btn':
          try:  # у некоторых кнопок нет pr['cmd']: команда присваивается позже
            cmd  = pr['cmd']
            match cmd['type']:
              case 'UIzoom'         : widget.config(command=lambda:_setUIzoom(True))
              case 'closeApp'       : widget.config(command=sysExit)
              case 'il:taskBtn'     : widget.config(
                command = lambda t=cmd['lmb']: _openTask_inRight(t)
                )
              case 'irFile:upd'     : widget.config(command=_updFile)
              case 'ir:launchBtn'   : widget.config(command=_launchClicked)
              case 'rbeEntry'       : widget.config(command=lambda:_suggFinalClicked(cmd['lmb']))
              case 'rbExit'         : widget.config(command=lambda:    self.buildUI('init',self))
              case 'rbfShowLog'     : widget.config(command=lambda:startfile(G.files['log']))
              case 'rbfShowErrors'  : widget.config(command=lambda:startfile(G.files['errors']))
              case 'rbeEntry:upCanc': widget.config(command=_suggRejectAllType)
          except: pass
    def _switchBoolSetting   (param:str):
      newVal = not G.config.get(param)
      G.config.set(param,newVal)
      if param == 'main:darkTheme': self.setUItheme(newVal)
    def _openTask_inRight    (type :str):
      # надо лишь закрывать при повторном нажатии, поэтому в отдельной функции
      def _build(): self.buildUI('ir',self.wx['fRoot'],{TO:type})

      self.destroyWidget('ir')
      TO,pr = 'curTask',self.props  # curTask = выбранная задача
      if TO in pr.keys():
        if  pr.pop(TO) != type: _build()
      else: _build()
    def _updFile             ():
      def _getProps():  # props = properties
        if book is None:
          FNC = S.UI['ir:fileNotChosen']
          return {'color' :'red',
                  'file'  : FNC,
                  'sheet' :'',
                  'btn'   : FNC,
                  'bState':'disabled'}
        else:
          return {'color' :'green',
                  'file'  : S.UI[keys['file' ]] + book['file'],
                  'sheet' : S.UI[keys['sheet']] + book['sheet'],
                  'btn'   : S.UI[keys['btn'  ]],
                  'bState':'normal'}

      keys = {'file' :'irFile:file',
              'sheet':'irFile:sheet',
              'btn'  :'ir:launchBtn'}
      book =  getCurExcel()
      p    = _getProps()
      for k    in ('file','sheet'): self.wx[keys[k]].config(foreground = G.UI.colors[p['color']])
      for k,it in     keys.items(): self.wx[it]     .config(text       = p[k])
      self.wx[keys['btn']].config(state=p['bState'])
      return book
    def _launchClicked       ():        # это запуск проверок
      book = _updFile()
      if book:
        # for param in G.launchTypes[type]['getOnLaunch']:
        #   G.config.set(type+':'+param,self.onLaunch[param].get())
        task = self.props['curTask']  # self.props очищается в self.buildUI()
        self   .buildUI('run',self)
        self.app.launch( book,task)
    def _suggFinalClicked    (btn:str): # btn = ok/cancel/rejectAll(отменить всю очередь)
      def _finish():
        self.destroyWidget('rbeVars')
        self.set_reLfr    (True)
        for w in self.getAllChilds(self.wx['fRoot']):
            for i in range(10): w.unbind(str(i))
        if btn == 'ok': OKcl,newVal = True ,VAL['value']
        else          : OKcl,newVal = False,''
        self.app.suggFinalClicked(OKcl,newVal)
        # case 'rejectAll':

      self.setErrorMsg()
      finish  = True
      if btn == 'ok':
        VAL = self.app.validate_andCapitalize(self.curError.type,
                                              self.wx['rbeEntry'].get())
        if not VAL['valid']: self.setErrorMsg(VAL); finish = False
      if finish: _finish()
    def _suggRejectAllType   ():
      while self.app.errors.queue: _suggFinalClicked('cancel')

    pr = G.UI.build[key]  # pr = properties
    _startRules()         # запуск особых правил (проверки внутри)
    widget = _createWidget()
    _bindCmd()            # внутри проверка по типу

    if 'pack'  in pr.keys(): widget.pack(**pr['pack'])  # не требуется для toolTip
    if 'wxKey' in pr.keys():
      wdg = widget.frame if pr['type'] == 'sfr' else widget
      self.wx[pr['wxKey']] = wdg
    if 'stash' in pr.keys():
      wdg = widget.frame if pr['type'] == 'sfr' else widget
      for  item in pr['stash']:
        if item != key: self.buildUI(item,wdg,params) # защита от зацикливания
    return    _finalRules() # запуск особых правил (проверки внутри)
  def destroyWidget(self,keys):  # в keys можно передать одну str либо tuple/list
    if  type(keys) == str: keys = [keys]
    for key in keys:
      try   : self.wx.pop(key).destroy()  # при первом запуске self.wx отсутствует
      except: pass
  def setUItheme   (self,theme:bool): # theme=true/false для выбора из G.UI.themes()
    self.style.theme_use(G.UI.themes     [theme])
    G.UI.colors        = G.UI.themeColors[theme]
  def finish       (self,totalErrors:int):
    self.destroyWidget(('rbRoot'))
    self.wx['rbLfr'].config(text=S.UI['rbFinished'],bootstyle='success')
    self.buildUI('rbf' ,self.wx['rbLfr'],
                {'text':replaceVars(S.UI['rbfLbl'],{'count':str(totalErrors)})})

  # работа с ошибками
  def  suggInvalidUD(self,queue,suggList:list):
    def _configWidgets():
      self.wx['rbe:curType'].config(text    = S.UI['rbe:curType'] + S.AStypes[errObj.type])
      self.wx['rbe:curBtn'] .config(text    = errObj.initVal,
                                    command = lambda:self.suggVarClicked(errObj.initVal))
      for w in self.getAllChilds(self.wx['fRoot']):
        w.bind('0',lambda s:self.suggVarClicked(errObj.initVal))
      self.set_reLfr()

    self.curError,errObj = queue[0],queue[0]  # надо запомнить, но чтобы здесь было проще
    _configWidgets()
    if suggList: self.buildUI('rbeVars',self.wx['rbRoot'],suggList)
    self.suggVarClicked(errObj.initVal) # добавляем в entry текущее значение
  def   setErrorMsg (self,vObj=None):   # показывает проблему введённого значения
    # vObj={type:,value:,valid:,errKey:}
    txt = '' if vObj is None else S.errInput[vObj['type']][vObj['errKey']]
    self.wx['rbe:errMsg'].config(text=txt)
  def      set_reLfr(self,disable=False):
    count = 0 if disable else len(self.app.errors.queue)
    self.wx['re'].config(text=replaceVars(S.UI['re:lfr'],{'count':str(count)}))
  def suggVarClicked(self,value:str):
    self.wx['rbeEntry'].delete(0,TBS.END)
    self.wx['rbeEntry'].insert(0,value)
    self.wx['rbeEntry:ok'].focus_set()
    self.setErrorMsg()

  # прочие, вспомогательные
  def log(self,string:str,unit:str):
    try   : color = G.UI.colors[G.UI.log[unit]]
    except: color = None
    self.buildUI('log',self.wx['rl:main'],{'text':string,'foreground':color})

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
