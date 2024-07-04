from   sys          import exit as SYSEXIT
from   tkinter              import BooleanVar
import ttkbootstrap             as TBS
from   ttkbootstrap.tooltip import ToolTip
import globalVars               as G
import strings                  as S
from   globalFuncs          import sysExit

# шаблоны моих классов (B=button)
class Btemplate(TBS.Button):
    def __init__(self,master,text=None,image=None,width=None,bootstyle='primary',command=None):
        super().__init__(master=master,command=command,text=text,image=image,width=width,bootstyle=bootstyle)
        self   .bind    ('<KeyPress-Return>',  command) # обрабатывает оба Enter'а (+numpad)
        self   .bind    ('<KeyPress-space>',   command)

# окно программы
class Window(TBS.Window):
    # конструкторы интерфейса
    def __init__(self):
        super().__init__(title     = G.app['TV'],
                         themename = G.app['themes'][G.config.get('main:darkTheme')],
                         size      = G.app['size'],
                         minsize   = G.app['size'])
        self.place_window_center()  # расположить в центре экрана
        self.buildInitUI()
    def buildInitUI(self):
        self.frRoot = TBS.Frame(self)
        self.frRoot.pack(fill='both',expand=True,padx=10,pady=10)
        self.buildFrame ('mainLeft' ,self.frRoot)
    def buildFrame(self,type:str,parent,params=None):
        # parent не всегда TBS.Frame; params нужен для buildTabs()
        if type == 'mainRight': self.frRight = TBS.Frame(parent)
        else:                   frMain       = TBS.Frame(parent)    # основной фрейм

        if   type == 'mainLeft':
            frMain.pack(fill='both',side='left',padx=5)
            self.buildFrame('MLfiles' ,frMain)  # выбор файла
            self.buildTabs            (frMain)  # кнопки запуска
            self.buildFrame('MLbottom',frMain)  # тема и закрытие программы
        elif type == 'MLfiles':
            frMain.pack(fill='x',pady=2)

            lbl           = TBS.Label   (frMain,text =S.layout['main']['lbl']['selectFile'])
            self.fileList = TBS.Combobox(frMain,width=33,bootstyle='success')

            pic           = TBS.PhotoImage(file=G.pics['filesUpdate'])
            btn           = Btemplate(frMain,image=pic,command=self.loadExcelList,bootstyle='link')
            btn.image     = pic # баг tkinter'a, нужно указать повторно
            ToolTip(btn,text=S.layout['main']['tt']['filesUpdate'])

            lbl          .pack(side='left',padx=8)
            btn          .pack(side='right')
            self.fileList.pack(pady=5)
            self     .loadExcelList ()
            self.fileList.focus_set ()
        elif type == 'MLtab':
            frMain.pack(fill='x')
            parent.add(frMain,text=S.layout['main']['tabs'][params],padding=7)
            for key,val in S.layout['actions'].items():
                bootstyle = 'success' if key == 'allChecks' else 'primary'
                if val['type'] == params:
                    Btemplate(frMain,
                              text      = val['btn'],
                              width     = 45,
                              command   = lambda k=key:self.actionClicked(k),
                              bootstyle = bootstyle
                              ).pack(pady=5)
        elif type == 'MLbottom':
            frMain.pack(fill='x',side='bottom',pady=5)
            self.buildFrame('MLtheme',frMain)
            Btemplate(frMain,
                      text      = S.layout['main']['btn']['closeApp'],
                      width     = 29,
                      command   = sysExit,
                      bootstyle = 'danger'
                      ).pack(side='left',padx=18)
        elif type == 'MLtheme':
            frMain.pack(side='left')

            for icon in G.pics['themeSelector'].values():
                pic       = TBS.PhotoImage(file=icon['pic'])
                lbl       = TBS.Label     (frMain,image=pic)
                lbl.image = pic # баг tkinter'a, нужно указать повторно
                lbl.pack(side=icon['side'],padx=icon['padx'])
            cb = TBS.Checkbutton(frMain,
                                 variable  = BooleanVar(value=G.config.get('main:darkTheme')),
                                 command   = lambda:self.switchBoolSetting('main:darkTheme'),
                                 bootstyle = 'round-toggle')
            ToolTip(cb,text=S.layout['main']['tt']['selectTheme'])
            cb.pack(expand=True)
    def buildTabs(self,parent:TBS.Frame):
            tabs  = TBS.Notebook(parent)
            tabs.pack(fill='both',expand=True,padx=7,pady=5)
            for type in ('main','script'): self.buildFrame('MLtab',tabs,type)

    # вспомогательные
    def loadExcelList(self):
        G.exBooks.update()
        if G.exBooks.cur:   # Excel открыт, и не только стартовый экран
            self.fileList.configure(values=G.exBooks.bookNames,state='readonly')
            self.fileList.set      (G.exBooks.cur)
        else:
            self.fileList.set      (S.layout['main']['msg']['noFilesFound'])
            self.fileList.configure(state='disabled')
        if hasattr(self,'frRight') and self.frRight.winfo_exists():
            self.frRight.setBtnState()

    # нажатия кнопок и переключателей
""" 
    def switchBoolSetting(self, param:str):
        newVal = not G.config.get(param)
        G.config.set(param, newVal)
        if param == 'main:darkTheme': self.style.theme_use(G.app['themes'][newVal])
    def actionClicked(self,type:str):
        sameClicked = False # если нажата та же кнопка, которая уже была выбрана, не открывать повторно
        if hasattr(self,'frRight'): # если правый фрейм существует
            sameClicked = self.frRight.winfo_exists() and type == self.frRight.type   А ЗДЕСЬ ЧТО?
            self.FRright.destroy()
        if not sameClicked:
            self.FRright = FRright(self, self.FRroot, S.layout['actions'][type]['lfl'], type)
            self.FRright.pack     (fill='both', expand=True, padx=6, pady=6,  side='right')
 """
# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
