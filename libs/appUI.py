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

class Window(TBS.Window):   # окно программы
    # конструкторы интерфейса
    def __init__(self,app):
        def bindSpace():
            def callDefault(event):
                try:
                    widget = self.nametowidget(event.widget)
                    widget.invoke()
                except KeyError: self.tk.call(event.widget,'invoke')
            self.bind_class('TButton','<Key-space>',callDefault,add='+')

        self.app = app  # для вызова функций класса Root() при нажатии кнопок
        super().__init__(title = G.UI.app['title'])
        self.setUItheme (G.config.get('main:darkTheme'))
        bindSpace    ()
        self.buildUI ('init',self)
        self.place_window_center()  # расположить в центре экрана
    def buildUI (self,key:str,parent):  # key = build key (из G.UI.build{})
        # создание интерфейса
        def startRules():
            try:
                if 'clean' in pr['rules']['start']:
                    try   :  self.wx['fRoot'].destroy()
                    except:  pass   # так проще, чем с доп. инициализацией self.wx и условиями
                    self.wx = {}    # здесь все ссылки на виджеты, которые надо хранить в памяти
            except: pass            # так проще, чем с доп. условиями
        def finalRules():
            try:
                if 'buildZoomBtn' in pr['rules']['final']: setUIzoom()
            except: pass    # так проще, чем с доп. условиями
        def bindCmd   ():
            # w = widget; key,pr = ключ и свойства из G.UI.build{}
            match pr['type']:
                case 'cb' : widget.configure(command=lambda:switchBoolSetting(pr['var']))
                case 'btn':
                    match key:
                        case 'btnCfgZoom' : widget.configure(command=lambda:setUIzoom(True))
                        case 'btnCloseApp': widget.configure(command=sysExit)
        # изменение оформления
        def setUIzoom (change=False):
            cfgName = 'main:zoom'
            sList   =  G.UI.sizes
            cur     =  G.config.get(cfgName)
            if change:
                cur += 1
                if cur == len(sList): cur = 0
                G .config.set(cfgName,cur)

            self.wx['btnCfgZoom'].configure(text = S.UI['inCfg:zoomBtn']+sList[cur]['lbl'])
            x,y = sList[cur]['size']
            self.geometry(str(x)+'x'+str(y))
            self.minsize (x,y)
        # кнопки и переключатели
        def switchBoolSetting(param:str):
            newVal = not G.config.get(param)
            G.config.set(param,newVal)
            if param == 'main:darkTheme': self.setUItheme(newVal)

        pr = G.UI.build[key]    # pr = properties
        startRules()            # запуск особых правил (проверки внутри)

        match pr['type']:
            case  'fr': widget = TBS.     Frame(parent)
            case 'lfr': widget = TBS.Labelframe(parent,**pr['build'])
            case 'lbl': widget = TBS.Label     (parent,**pr['build'])
            case 'btn': widget = TBS.Button    (parent,**pr['build'])
            case 'tt' : widget =     ToolTip   (parent,**pr['build'])
            case 'cb' :
                widget = TBS.Checkbutton(
                    parent,
                    variable = BooleanVar(value=G.config.get(pr['var'])),
                    **pr['build']
                    )
        bindCmd()   # внутри проверка по типу

        if 'pack'  in pr.keys(): widget.pack(**pr['pack'])  # не требуется для toolTip
        if 'wxKey' in pr.keys(): self.wx[pr['wxKey']] = widget
        if 'stash' in pr.keys():
            for    item in pr['stash']:
                if item != key: self.buildUI(item,widget)   # защита от зацикливания
        finalRules()    # запуск особых правил (проверки внутри)

    # изменение оформления
    def setUItheme(self,theme:bool):    # theme=true/false для выбора из G.UI.themes()
        self.style.theme_use(G.UI.themes     [theme])
        G.UI.colors        = G.UI.themeColors[theme]

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
