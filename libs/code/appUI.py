from   sys          import exit as SYSEXIT
from   tkinter              import BooleanVar
import ttkbootstrap             as TBS
from   ttkbootstrap.tooltip import ToolTip
import strings                  as S
import globalVars               as G
from   globalFuncs          import sysExit
from   launchFuncs          import launchScript

# шаблоны моих классов (B=button, FR=frame, LFR=labelFrame)
class Btemplate(TBS.Button):
    def __init__(self, master, text=None, image=None, width=None, bootstyle='primary', command=None):
        super().__init__(master=master, command=command, text=text, image=image, width=width, bootstyle=bootstyle)
        self   .bind    ('<KeyPress-Return>',   command)    # обрабатывает оба Enter'а (+numpad)
        self   .bind    ('<KeyPress-space>',    command)
class FRtemplate(TBS.Frame):
    def __init__(self, app, master):
        self.app = app  # для вызова функций основного окна
        super().__init__(master)
        self.build()
class LFRtemplate(TBS.Labelframe):
    def __init__(self, app, master, text:str, type:str=None):
        self.app  = app     # для вызова функций основного окна
        self.type = type
        super().__init__(master, text=text)
        self.build()

# окно программы
class Window(TBS.Window):
    def __init__(self):
        super().__init__(title=G.app['TV'], themename=G.app['themes'][G.config.get('main:darkTheme')])
        self.setGeometry()
        self.buildFrames()
    def setGeometry(self):
        x, y = G.app['size']
        self.geometry (str(x) + 'x' + str(y))   # задаём размеры окна
        self.resizable(False, False)            # нельзя менять размеры окна
        self.place_window_center  ()            # расположить в центре экрана
    def buildFrames(self):
        self.FRroot = TBS.Frame(self)
        self.FRleft = FRleft   (self, self.FRroot)
        self.FRroot.pack(fill='both', expand=True, padx=10, pady=10)
        self.FRleft.pack(fill='both', side='left', padx=5)
    def switchBoolSetting(self, param:str):
        newVal = not G.config.get(param)
        G.config.set(param, newVal)
        if param == 'main:darkTheme': self.style.theme_use(G.app['themes'][newVal])
    def actionClicked(self, type:str):
        sameClicked = False             # если нажата та же кнопка, которая уже была выбрана, не открывать повторно
        if hasattr(self, 'FRright'):    # если FRright существует
            sameClicked = self.FRright.winfo_exists() and type == self.FRright.type
            self.FRright.destroy()
        if not sameClicked:
            self.FRright = FRright(self, self.FRroot, S.layout['actions'][type]['lfl'], type)
            self.FRright.pack     (fill='both', expand=True, padx=6, pady=6,  side='right')
    def launch(self, type:str): # это запуск проверок
        book = G.exBooks.getFile(self.FRleft.FRfile.list.get())
        if book == None:
            self.FRright.btn.configure(text=S.layout['main']['btn']['launch']['cantLaunch'], state='disabled')
        else:
            self.buildRunUI()
            launchScript   (book, type, self.FRlog, self.FRerrors)
    def buildRunUI(self):
        self.FRleft .destroy()
        self.FRright.destroy()
        self.FRlog    = FRlog   (self, self.FRroot, S.layout['run']['log'])
        self.FRerrors = FRerrors(self, self.FRroot)
        self.FRlog   .pack      (fill='both', expand=True, side='left' , padx=5)
        self.FRerrors.pack      (fill='both', expand=True, side='right', padx=5)

# фреймы основного окна (FR=frame)
class FRleft(FRtemplate):
    def build(self):
        self.FRfile    = FRfile      (self.app, self)
        tabs           = TBS.Notebook(self)
        downFrame      = FRbottom    (self.app, self)
        self.FRfile   .pack          (fill='x', pady=2)
        tabs          .pack          (fill='x', padx=7,        pady=2)
        downFrame     .pack          (fill='x', side='bottom', pady=5)

        for type in ('main', 'script'):
            frTab = FRactions(self.app, tabs, type)
            frTab.pack       (fill='x')
            tabs.add(frTab, text=S.layout['main']['tabs'][type], padding=7)
class FRfile(FRtemplate):
    def __init__(self, app, master):
        super().__init__(app, master)
        self.loadExcelList()
    def build(self):
        lbl       = TBS.Label     (self, text =S.layout['main']['lbl']['selectFile'])
        self.list = TBS.Combobox  (self, width=33, bootstyle='success')

        pic       = TBS.PhotoImage(file=G.pics['filesUpdate'])
        btn       = Btemplate     (self, image=pic, command=self.loadExcelList, bootstyle='link')
        btn.image = pic # баг tkinter'a, нужно указать повторно
        ToolTip(btn, text=S.layout['main']['tt']['filesUpdate'])

        lbl      .pack(side='left', padx=8)
        btn      .pack(side='right')
        self.list.pack(pady=5)
        self.list.focus_set()
    def loadExcelList(self):
        G.exBooks.update()
        if G.exBooks.cur:   # Excel открыт, и не только стартовый экран
            self.list.configure(values=G.exBooks.bookNames, state='readonly')
            self.list.set      (G.exBooks.cur)
        else:
            self.list.set      (S.layout['main']['msg']['noFilesFound'])
            self.list.configure(state='disabled')
        if hasattr(self.app, 'FRright') and self.app.FRright.winfo_exists():
            self.app.FRright.setBtnState()
class FRactions(FRtemplate):
    def __init__(self, app, master, type:str):
        self.type = type
        super().__init__(app, master)
    def build(self):
        for key, val in S.layout['actions'].items():
            bootstyle = 'primary'
            if   key == 'allChecks': bootstyle = 'success'
            if val['type'] == self.type:
                Btemplate(self, text=val['btn'], width=45, command=lambda k=key:self.app.actionClicked(k), bootstyle=bootstyle).pack(pady=5)
class FRbottom(FRtemplate):
    def build(self):
        self.FRtheme = FRtheme  (self.app, self)
        btn          = Btemplate(self, text=S.layout['main']['btn']['closeApp'], width=29, command=sysExit, bootstyle='danger')
        self.FRtheme.pack       (side='left')
        btn         .pack       (side='left', padx=18)
class FRtheme(FRtemplate):
    def build(self):
        for icon in G.pics['themeSelector'].values():
            pic       = TBS.PhotoImage(file=icon['pic'])
            lbl       = TBS.Label     (self, image=pic)
            lbl.image = pic # баг tkinter'a, нужно указать повторно
            lbl.pack(side=icon['side'], padx=icon['padx'])
        cb = TBS.Checkbutton(self,
                             variable  = BooleanVar    (value=G.config.get('main:darkTheme')),
                             command   = lambda:self.app.switchBoolSetting('main:darkTheme'),
                             bootstyle = 'round-toggle')
        ToolTip(cb, text=S.layout['main']['tt']['selectTheme'])
        cb.pack(expand=True)
class FRright(LFRtemplate):
    def build(self):
        descr           = TBS.Label   (self,     text=S.layout['actions'][self.type]['descr'], wraplength=320)
        self.FRsettings = FRactionsCfg(self.app, self)
        self.btn        = Btemplate   (self, command=lambda t=self.type:self.app.launch(t), bootstyle='success')
        descr          .pack(fill='x', padx=8,  pady=5)
        self.FRsettings.pack(fill='x', padx=8)
        self.btn       .pack(fill='x', padx=22, pady=12, side='bottom')
        self.setBtnState()
    def setBtnState(self):
        if G.exBooks.cur: self.btn.configure(text=S.layout['main']['btn']['launch']['ready']    , state='normal')
        else:             self.btn.configure(text=S.layout['main']['btn']['launch']['notChosen'], state='disabled')
class FRactionsCfg(FRtemplate):
    def build(self):
        for group in ('forAll', self.master.type):  # self.master.type = например, 'checkTitles'
            if group in S.layout['actionsCfg'].keys():
                TBS .Separator (self ).pack(fill='x', padx=2, pady=6)
                self.buildGroup(group)
    def buildGroup(self, group:str):
        for type, strings in S.layout['actionsCfg'][group].items():
            sType = self.master.type + ':' + type   # например, 'checkTitles:newSheet'
            cb    = TBS.Checkbutton(self,
                                    text      = strings['lbl'],
                                    variable  = BooleanVar        (value=G.config.get(sType)),
                                    command   = lambda t=sType:self.app.switchBoolSetting(t),
                                    bootstyle = 'round-toggle')
            ToolTip(cb, text=strings['tt'])
            cb.pack(padx=5, pady=5, expand=True, anchor='w')

# фреймы выполнения скриптов
class FRlog(LFRtemplate):   # общие функции FRlog и FRerrors
    def build(self):
        self.frame = TBS.Frame(self)
        self.frame.pack(fill='both', expand=True, padx=10, pady=5)
    def add(self, string):
        TBS.Label(self.frame, text=string).pack(fill='x')
class FRerrors(FRlog):
    def __init__(self, app, master):
        self.storage = {}   # {type:{initLow:LabelObj,...},...}
        super().__init__(app, master, S.layout['run']['errors'])
    def add(self, type, key, string):
        if type not in self.storage.keys(): self.storage[type] = {}
        self.storage[type][key] = TBS.Label(self.frame, text=string)
        self.storage[type][key].pack(fill='x')
    def suggest(self):
        pass

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
