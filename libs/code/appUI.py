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
    def __init__(self,app):
        self.app = app  # для вызова функций класса Root() при нажатии кнопок
        super().__init__(title     = G.app['TV'],
                         themename = G.app['themes'][G.config.get('main:darkTheme')],
                         size      = G.app['size'],
                         minsize   = G.app['size'])
        self.place_window_center()  # расположить в центре экрана
        self.buildInitUI()
    def buildInitUI(self):
        self.frRight = None # сначала это: он читается в self.loadExcelList()
        self.frRoot  = TBS.Frame(self)
        self.frRoot.pack(fill='both',expand=True,padx=10,pady=10)
        self.buildFrame ('mainLeft' ,self.frRoot)
    def buildRunUI(self):
        pass
    def buildFrame(self,type:str,parent,params=None):
        # frMain = TBS.Frame либо TBS.Labelframe
        if   type == 'mainLeft':
            frMain = TBS.Frame(parent)
            frMain.pack(fill='both',side='left',padx=5)
            self.buildFrame('MLfiles' ,frMain)  # выбор файла
            self.buildTabs            (frMain)  # кнопки запуска
            self.buildFrame('MLbottom',frMain)  # тема и закрытие программы
        elif type == 'MLfiles':
            frMain =   TBS.Frame(parent)
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
            frMain = TBS.Frame(parent)
            frMain.pack       (fill='x')
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
            frMain = TBS.Frame(parent)
            frMain.pack(fill='x',side='bottom',pady=5)
            self.buildFrame('MLtheme',frMain)
            Btemplate(frMain,
                      text      = S.layout['main']['btn']['closeApp'],
                      width     = 29,
                      command   = sysExit,
                      bootstyle = 'danger'
                      ).pack(side='left',padx=18)
        elif type == 'MLtheme':
            frMain = TBS.Frame(parent)
            frMain.pack  (side='left')

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
        elif type == 'mainRight':
            # в params передан тип (напр., 'checkEmails')
            strings = S.layout['actions'][params]
            frMain  = TBS.Labelframe(parent,text=strings['lfl'])
            frMain.pack (fill='both',expand=True,padx=6,pady=6,side='right')
            TBS   .Label(frMain, text=strings['descr']).pack(fill='x',padx=8,pady=5)
            self  .buildFrame('MRconfig',frMain,params)
            self  .launchBtn = Btemplate(frMain,command=lambda t=params:self.launchClicked(t),bootstyle='success')
            self  .launchBtn.pack       (fill='x',padx=22,pady=12,side='bottom')
            self  .setLaunchBtnState()
            return frMain   # только в mainRight, чтобы записать в self.frRight['frame']
        elif type == 'MRconfig':
            # в params передан тип (напр., 'checkEmails')
            frMain = TBS.Frame(parent)
            frMain .pack (fill='x',padx=8)
            for group in ('forAll',params):
                if group in S.layout['actionsCfg'].keys():
                    TBS .Separator(frMain).pack(fill='x',padx=2,pady=6)
                    self.buildActionsCfgGroup  (frMain  ,params,group)
    def buildTabs(self,parent:TBS.Frame):
            tabs  = TBS.Notebook(parent)
            tabs.pack(fill='both',expand=True,padx=7,pady=5)
            for type in ('main','script'): self.buildFrame('MLtab',tabs,type)
    def buildActionsCfgGroup(self,parent:TBS.Frame,type:str,group:str):
        for param,strings in S.layout['actionsCfg'][group].items():
            sType = type+':'+param  # например, 'checkTitles:newSheet'
            cb    = TBS.Checkbutton(parent,
                                    text      = strings['lbl'],
                                    variable  = BooleanVar    (value=G.config.get(sType)),
                                    command   = lambda t=sType:self.switchBoolSetting(t),
                                    bootstyle = 'round-toggle')
            ToolTip(cb,text=strings['tt'])
            cb.pack(padx=5,pady=5,expand=True,anchor='w')

    # вспомогательные
    def loadExcelList(self):
        G.exBooks.update()
        if G.exBooks.cur:   # Excel открыт, и не только стартовый экран
            self.fileList.configure(values=G.exBooks.bookNames,state='readonly')
            self.fileList.set      (G.exBooks.cur)
        else:
            self.fileList.set      (S.layout['main']['msg']['noFilesFound'])
            self.fileList.configure(state='disabled')
        if self.frRight is not None: self.setLaunchBtnState()

    # кнопки и переключатели
    def switchBoolSetting(self,param:str):
        newVal = not G.config.get(param)
        G.config.set(param,newVal)
        if param == 'main:darkTheme': self.style.theme_use(G.app['themes'][newVal])
    def setLaunchBtnState(self):
        if G.exBooks.cur: self.launchBtn.configure(text=S.layout['main']['btn']['launch']['ready']    ,state='normal')
        else:             self.launchBtn.configure(text=S.layout['main']['btn']['launch']['notChosen'],state='disabled')
    def actionClicked(self,type:str):
        if    self.frRight is not None: self.frRight['frame'].destroy()
        if    self.frRight is not None and type == self.frRight['type']:    # выбран тот же тип проверки
              self.frRight = None
        else: self.frRight = {'type':type, 'frame':self.buildFrame('mainRight',self.frRoot,type)}
    def launchClicked(self,type:str):   # это запуск проверок
        book     = G.exBooks.getFile(self.fileList.get())
        if book == None:
            self.launchBtn.configure(text=S.layout['main']['btn']['launch']['cantLaunch'],state='disabled')
        else:
            self.buildRunUI()
            self.app.launch(book,type)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
