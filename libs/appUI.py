from   sys                          import exit as SYSEXIT
from   tkinter                      import BooleanVar
import ttkbootstrap                     as TBS
from   ttkbootstrap.tooltip         import ToolTip
from   ttkbootstrap.dialogs.dialogs import Messagebox
import globalsMain                      as G
import strings                          as S
from   globalFuncs                  import sysExit

def cantReadLib(): Messagebox.ok(S.UI['init']['msg']['cantReadLib'],G.UI.app['title'])

class Window(TBS.Window):   # окно программы
    # конструкторы интерфейса
    def __init__  (self,app):
        self.app = app  # для вызова функций класса Root() при нажатии кнопок
        super().__init__(title = G.UI.app['title'])
        self.setUItheme (G.config.get('main:darkTheme'))
        self.bindSpace()
        self.buildUI  ('init',self)
        # self.setUIzoom()    # обязательно после buildUI() (обновляется кнопка)
        self.place_window_center()  # расположить в центре экрана
    def bindSpace (self):
        def callDefault(event):
            try:
                widget = self.nametowidget(event.widget)
                widget.invoke()
            except KeyError: self.tk.call(event.widget,'invoke')

        self.bind_class('TButton','<Key-space>',callDefault,add='+')
    def buildUI   (self,key:str,parent):    # key = build key (из G.UI.build{})
        pr = G.UI.build[key]    # pr = properties
        self.cleanUI(pr)        # внутри проверка (есть ли 'clean' в списке 'rules')

        match pr['type']:
            case 'fr' : widget = TBS.     Frame (parent)
            case 'lfr': widget = TBS.Labelframe (parent,text=S.UI[pr['title']])
            case 'lbl': widget = TBS.Label      (parent,**pr['build'])
            case 'cb' :
                widget = TBS.Checkbutton(
                    parent,
                    variable = BooleanVar(value=G.config.get(pr['var'])),
                    **pr['build']
                    )
                ToolTip(widget,text=S.UI[pr['tt']])
        widget.pack(**pr['pack'])
        self.bindCmd(widget,key,pr) # внутри проверка по типу

        if 'wxKey' in pr.keys(): self.wx[pr['wxKey']] = widget
        if 'stash' in pr.keys():
            for    item in pr['stash']:
                if item != key: self.buildUI(item,widget)   # защита от зацикливания
    def cleanUI(self,scheme:dict):
        if 'rules' in scheme.keys() and 'clean' in scheme['rules']:
            try   : self.wx['fRoot'].destroy()
            except: pass    # так проще, чем с доп. инициализацией self.wx и условиями
            self.wx = {}    # здесь все ссылки на виджеты, которые надо хранить в памяти
    def bindCmd(self,widget,key:str,pr:dict):   # key,pr = ключ и свойства из G.UI.build{}
        match pr['type']:
            case 'cb': widget.configure(command=lambda:self.switchBoolSetting(pr['var']))

    # изменение оформления
    def setUItheme(self,theme:bool):    # theme=true/false для выбора из G.UI.themes()
        self.style.theme_use(G.UI.themes     [theme])
        G.UI.colors        = G.UI.themeColors[theme]
    def setUIzoom (self,change=False):
        cfgName = 'main:zoom'
        sList   =  G.UI.sizes
        cur     =  G.config.get(cfgName)
        if change:
            cur += 1
            if cur == len(sList): cur = 0
            G .config.set(cfgName,cur)

        self.zoomBtn.configure(text = S.UI['init']['btn']['cfgZoom'] + sList[cur]['lbl'])
        x,y = sList[cur]['size']
        self.geometry(str(x)+'x'+str(y))
        self.minsize (x,y)

    # кнопки и переключатели
    def switchBoolSetting(self,param:str):
        newVal = not G.config.get(param)
        G.config.set(param,newVal)
        if param == 'main:darkTheme': self.setUItheme(newVal)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
