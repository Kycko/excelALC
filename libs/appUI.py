from   sys                          import exit as SYSEXIT
from   tkinter                      import BooleanVar
import ttkbootstrap                     as TBS
from   ttkbootstrap.tooltip         import ToolTip
from   ttkbootstrap.dialogs.dialogs import Messagebox
import globalsMain                      as G
import strings                          as S
from   globalFuncs                  import sysExit

def cantReadLib():
  Messagebox.ok(S.UI['init:cantReadLib'].replace('$FILE$',G.files['lib']),
                G.UI.app['title'])

class Window(TBS.Window): # окно программы
  # конструкторы интерфейса
  def __init__  (self,app):
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
  def buildUI   (self,key:str,parent,params=None):
    # key = build key (из G.UI.build{})
    # в params передаём любые доп. данные (напр., тип задачи для фрейма 'ir')
    # создание интерфейса
    def _startRules  ():
      try:
        rules = pr['rules']['start']
        if 'clean'     in rules:
          try   : self.wx.pop('fRoot').destroy()
          except: pass  # так проще, чем с доп. инициализацией self.wx и условиями
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
      try:
        rules = pr['rules']['final']
        if 'packTab'       in rules: parent.add(widget,**pr['packTab'])
        if 'build:zoomBtn' in rules: _setUIzoom()
        if 'build:ir'      in rules:
          tOp = S.UI['tasks'][self.props['curTask']]
          for widg in ('ir','irDesc'): self.wx[widg].configure(text=tOp[widg])
        if 'build:irCfg'   in rules:
          for wKey in G.UI.irCfg[self.props['curTask']]: self.buildUI(wKey,widget)
      except: pass  # так проще, чем с доп. условиями
    def _createWidget():
      bld = pr['build'] if 'build' in pr.keys() else {}
      match pr['type']:
        case  'fr': return TBS.     Frame(parent)
        case 'lfr': return TBS.Labelframe(parent,**bld)
        case 'lbl': return TBS.Label     (parent,**bld)
        case 'btn': return TBS.Button    (parent,**bld)
        case 'tt' : return     ToolTip   (parent,**bld)
        case 'tbs': return TBS.Notebook  (parent)
        case 'sep': return TBS.Separator (parent)
        case 'cb' :
          return TBS.Checkbutton(
            parent,
            variable = BooleanVar(value=G.config.get(pr['var'])),
            **bld
            )
    # изменение оформления
    def _setUIzoom(change=False):
      cfgName = 'main:zoom'
      sList   =  G.UI.sizes
      cur     =  G.config.get(cfgName)
      if change:
        cur += 1
        if cur == len(sList): cur = 0
        G .config.set(cfgName,cur)

      self.wx['cfgZoom'].configure(text = S.UI['ilCfg:zoomBtn']+sList[cur]['lbl'])
      x,y = sList[cur]['size']
      self.geometry(str(x)+'x'+str(y))
      self.minsize (x,y)
    # кнопки и переключатели
    def _bindCmd():
      # w = widget; key,pr = ключ и свойства из G.UI.build{}
      match pr['type']:
        case 'cb' : widget.configure(command=lambda:_switchBoolSetting(pr['var']))
        case 'btn':
          cmd  =  pr['cmd']
          match  cmd['type']:
            case    'UIzoom': widget.configure(command=lambda:_setUIzoom(True))
            case  'closeApp': widget.configure(command=sysExit)
            case 'ilTaskBtn': widget.configure(
              command = lambda t=cmd['lmb']: self.openTask_inRight(t)
              )
    def _switchBoolSetting(param:str):
      newVal = not G.config.get(param)
      G.config.set(param,newVal)
      if param == 'main:darkTheme': self.setUItheme(newVal)

    pr = G.UI.build[key]  # pr = properties
    _startRules()         # запуск особых правил (проверки внутри)
    widget = _createWidget()
    _bindCmd()            # внутри проверка по типу

    if 'pack'  in pr.keys(): widget.pack(**pr['pack'])  # не требуется для toolTip
    if 'wxKey' in pr.keys(): self.wx[pr['wxKey']] = widget
    if 'stash' in pr.keys():
      for  item in pr['stash']:
        if item != key: self.buildUI(item,widget) # защита от зацикливания
    _finalRules() # запуск особых правил (проверки внутри)
  def setUItheme(self,theme:bool):  # theme=true/false для выбора из G.UI.themes()
    self.style.theme_use(G.UI.themes     [theme])
    G.UI.colors        = G.UI.themeColors[theme]
  def openTask_inRight(self,type:str):
    # надо лишь закрывать при повторном нажатии, поэтому в отдельной функции
    def _build(): self.buildUI('ir',self.wx['fRoot'],{TO:type})

    try   : self.wx.pop('ir').destroy()
    except: pass
    TO,pr = 'curTask',self.props  # curTask = выбранная задача
    if TO in pr.keys():
      if  pr.pop(TO) != type: _build()
    else: _build()

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
