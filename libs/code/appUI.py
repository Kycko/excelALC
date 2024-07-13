from   sys                  import exit as SYSEXIT
from   tkinter                      import BooleanVar
import ttkbootstrap                     as TBS
from   ttkbootstrap.tooltip         import ToolTip
from   ttkbootstrap.dialogs.dialogs import Messagebox
import globalVars                       as G
import strings                          as S
from   globalFuncs                  import sysExit

def cantReadLib(): Messagebox.ok(S.layout['main']['msg']['cantReadLib'],G.app['TV'])

class Btemplate(TBS.Button):    # шаблон кнопки
    def __init__(self,master,text=None,image=None,width=None,bootstyle='primary',command=None):
        super().__init__(master=master,command=command,text=text,image=image,width=width,bootstyle=bootstyle)
        self   .bind    ('<KeyPress-Return>',  command) # обрабатывает оба Enter'а (+numpad)
        self   .bind    ('<KeyPress-space>',   command)
class Window(TBS.Window):       # окно программы
    # конструкторы интерфейса
    def __init__(self,app):
        self.app = app  # для вызова функций класса Root() при нажатии кнопок
        super().__init__(title     = G.app['TV'],
                         themename = G.app['themes'][G.config.get('main:darkTheme')],
                         size      = G.app['size'],
                         minsize   = G.app['size'])
        self.place_window_center()  # расположить в центре экрана
        self.buildUI()
    def buildUI(self,runUI=False):  # runUI = окно выбора (False) или окно выполнения (True)
        if hasattr(self,'frRoot'): self.frRoot.destroy()
        self.frRight = None # сначала это: он читается в self.loadExcelList()
        self.frRoot  = TBS.Frame(self)
        self.frRoot.pack(fill='both',expand=True,padx=10,pady=10)
        self.buildFrame (('mainLeft','mainRun')[runUI],self.frRoot)
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
        elif type == 'mainRun':
            frMain = TBS.Frame(parent)
            frMain.pack(fill='y',side='right',padx=5)
            self.buildFrame('runLog'   ,parent) # основной журнал выполнения
            self.buildFrame('runSugg'  ,frMain) # предложения по исправлению ошибок
            self.buildFrame('runErrors',frMain) # список текущих ошибок
        elif type == 'runLog':
            frMain = TBS.Labelframe(parent,text=S.layout['run']['lfl']['mainLog'])
            frMain      .pack (fill='both',expand=True,side='left',padx=5 ,pady=4)
            self.frLog = TBS.Frame(frMain)  # внутренний фрейм с нужными отступами
            self.frLog.pack(fill='both',expand=True,padx=10,pady=5)
        elif type == 'runErrors':
            frMain = TBS.Labelframe(parent,text=S.layout['run']['lfl']['errors'])
            frMain.pack(fill='both',expand=True,pady=4)
            self.errors = Errors(frMain)
        elif type == 'runSugg':
            self.suggLfl = TBS.Labelframe(parent)       # в нём будем писать счётчик ошибок
            self.suggLfl.pack   (fill='x',pady=5)
            self.setSuggTitle()
            frSugg     = TBS.Frame(self.suggLfl)
            frSugg.pack(fill='x',padx=10,pady=5)
            self.suggWidgets = {}                       # все виджеты, которые надо включать/отключать
            self.buildFrame('runSugg_curVal',frSugg)    # фрейм вывода текущего значения
            self.buildFrame('runSuggVars'   ,frSugg)    # фрейм для добавления кнопок выбора
            self.buildFrame('runSuggEntry'  ,frSugg)    # фрейм с полем ручного ввода текста
        elif type == 'runSugg_curVal':
            frMain = TBS.Frame(parent)
            frMain.pack     (fill='x')
            strings = S.layout['run']['suggUI']['curValue']
            TBS.Label(frMain,text=strings['lbl']).pack(side='left')
            self.suggWidgets['curVal'] = Btemplate(frMain,text=strings['btn'],bootstyle='outline')
            self.suggWidgets['curVal'].pack(fill='x',side='right')
        elif type == 'runSuggVars':
            self.frSuggVars = TBS.Frame(parent)
            self.frSuggVars.pack     (fill='x')
            #TBS.Label(parent,text=S.layout['run']['suggUI']['vars']).pack(fill='x')
        elif type == 'runSuggEntry':
            frMain = TBS.Frame(parent)
            frMain.pack     (fill='x')
            TBS.Separator(frMain).pack(fill='x',pady=7)
            TBS.Label(frMain,text=S.layout['run']['suggUI']['lblEntry']).pack(fill='x')
            self.suggWidgets['entry']   = TBS.Entry(frMain)
            self.suggWidgets['entry'].pack(fill='x',pady=7)
            self.buildFrame('runSugg_entryButtons',frMain)  # кнопки ОК и Отмена
            self.setSuggState(False)
        elif type == 'runSugg_entryButtons':
            frMain = TBS.Frame(parent)
            frMain.pack     (fill='x',pady=3)
            for key,cfg in S.layout['run']['suggUI']['buttons'].items():
                self.suggWidgets[key] = Btemplate(frMain,
                                                  text      = cfg['text'],
                                                  command   = lambda key=key:self.suggEntered(key),
                                                  bootstyle = cfg['style'])
                self.suggWidgets[key].pack(side='right',padx=cfg['padx'])
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
    def log(self,string:str): TBS.Label(self.frLog,text=string).pack(fill='x')
    def loadExcelList (self):
        G.exBooks.update()
        if G.exBooks.cur:   # Excel открыт, и не только стартовый экран
            self.fileList.configure(values=G.exBooks.bookNames,state='readonly')
            self.fileList.set      (G.exBooks.cur)
        else:
            self.fileList.set      (S.layout['main']['msg']['noFilesFound'])
            self.fileList.configure(state='disabled')
        if self.frRight is not None: self.setLaunchBtnState()
    def setSuggTitle(self,counter:dict=None):   # counter = {'cur':,'total':}
        if counter is None: numbers = ''
        else:
            numbers = S.layout['run']['suggUI']['counter']
            numbers = numbers.replace('$$2',str(counter['cur'])).replace('$$3',str(counter['total']))
        self.suggLfl.configure(text=S.layout['run']['lfl']['sugg'].replace('$$1',numbers))
    def setSuggState(self,enabled:bool):
        for widget in self.suggWidgets.values(): widget.configure(state=('disabled','normal')[enabled])
    def suggInvalidUD(self,type:str,initVal:str,suggList:list,counter:dict):
        # counter = {'cur':,'total':}
        self.setSuggTitle(counter)
        self.setSuggState(True)
        self.suggWidgets['curVal'].configure(text=initVal,command=lambda s=initVal:self.suggCurClicked(s))
        self.suggCurClicked(initVal)    # добавляем в entry текущее значение

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
            self   .buildUI(True)
            self.app.launch(book,type)
    def suggCurClicked(self,value):
        self.suggWidgets['entry'].delete(0,TBS.END)
        self.suggWidgets['entry'].insert(0,value)
    def suggEntered(self,bttn:str):     # bttn = либо 'ok', либо 'cancel'
        pass
class Errors(): # фрейм ошибок
    def __init__(self,parent:TBS.Labelframe):
        self.storage = {}                   # {type:{initLow:TBS.Label,...},...}
        self.frame   = TBS.Frame(parent)    # внутренний фрейм с нужными отступами
        self.frame.pack(fill='both',expand=True,padx=10,pady=5)
    def add(self,type:str,low:str,text:str):
        if type not in self.storage.keys(): self.storage[type] = {}
        self.storage[type][low] = TBS.Label(self.frame,text=text)
        self.storage[type][low].pack(fill='x')

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
