from   sys                  import exit as SYSEXIT
from   tkinter                      import BooleanVar,StringVar
import ttkbootstrap                     as TBS
from   ttkbootstrap.tooltip         import ToolTip
from   ttkbootstrap.dialogs.dialogs import Messagebox
import globalVars                       as G
import strings                          as S
from   globalFuncs                  import sysExit

def cantReadLib(): Messagebox.ok(S.layout['main']['msg']['cantReadLib'],G.app['TV'])

class Window(TBS.Window):   # окно программы
    # конструкторы интерфейса
    def __init__(self,app):
        self.app = app  # для вызова функций класса Root() при нажатии кнопок
        super().__init__(title     = G.app['TV'],
                         themename = G.app['themes'][G.config.get('main:darkTheme')],
                         size      = G.app['size'],
                         minsize   = G.app['size'])
        self.bindSpace()
        self.place_window_center()  # расположить в центре экрана
        self.buildUI()
    def bindSpace(self):
        def callDefault(event):
            try:
                widget = self.nametowidget(event.widget)
                widget.invoke()
            except KeyError: self.tk.call(event.widget,'invoke')

        self.bind_class('TButton','<Key-space>',callDefault,add='+')
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
            btn           = TBS.Button(frMain,image=pic,command=self.loadExcelList,bootstyle='link')
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
                if val['type'] == params:
                    TBS.Button(frMain,
                              text      = val['btn'],
                              width     = 45,
                              command   = lambda k=key:self.actionClicked(k),
                              bootstyle = val['style']
                              ).pack(pady=5)
        elif type == 'MLbottom':
            frMain = TBS.Frame(parent)
            frMain.pack(fill='x',side='bottom',pady=5)
            self.buildFrame('MLtheme',frMain)
            TBS.Button(frMain,
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
            TBS   .Label(frMain,text=strings['descr'],wraplength=620).pack(fill='x',padx=8,pady=5)
            self  .buildFrame('MRconfig',frMain,params)
            self  .launchBtn = TBS.Button(frMain,command=lambda t=params:self.launchClicked(t),bootstyle='success')
            self  .launchBtn.pack       (fill='x',padx=22,pady=12,side='bottom')
            self  .setLaunchBtnState()
            return frMain   # только в mainRight, чтобы записать в self.frRight['frame']
        elif type == 'MRconfig':
            # в params передан тип (напр., 'checkEmails')
            frMain = TBS.Frame(parent)
            frMain .pack (fill='x',padx=8)
            for group in ('forAll',params):
                if group in S.layout['actionsCfg'].keys():
                    self.buildSeparator      (frMain,padx=2,pady=6)
                    self.buildActionsCfgGroup(frMain,params,group)

            GOL = G.launchTypes[params]['getOnLaunch']
            if GOL:
                self.buildSeparator     (frMain,padx=2,pady=6)
                self.buildOnLaunchInputs(frMain,params,GOL)
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
            self.suggLfl = TBS.Labelframe(parent,text=S.layout['run']['lfl']['sugg'])
            self.suggLfl.pack   (fill='x',pady=5)
            self.frSugg = TBS.Frame(self.suggLfl)
            self.frSugg.pack (fill='x',padx=10,pady=2)
            self.buildFrame('runSuggType'   ,self.frSugg)
            self.suggWidgets = {}                           # все виджеты, которые надо включать/отключать
            self.buildFrame('runSugg_curVal',self.frSugg)   # фрейм вывода текущего значения

            self.frSuggMain = TBS.Frame(self.frSugg)    # чтобы фрейм предложений оставался при удалении данных
            self.frSuggMain.pack(fill='x')
            # ↓ чтобы фрейм предложений сжимался после удаления всех предложений
            TBS.Frame(self.frSuggMain,height=1,width=1).pack(fill='x')
            self.buildFrame('runSuggVars' ,self.frSuggMain,[])  # фрейм для добавления кнопок выбора
            self.buildFrame('runSuggEntry',self.frSugg)         # фрейм с полем ручного ввода текста
        elif type == 'runSuggType':
            frMain = TBS.Frame(parent)
            frMain.pack     (fill='x')
            TBS.Label(frMain,
                      foreground = G.colors['lightRed'],
                      text       = S.layout['run']['suggUI']['errType']
                      ).pack(side='left')
            self.lblSuggType = TBS.Label(frMain,foreground=G.colors['lightRed'])
            self.lblSuggType.pack (side='left')
        elif type == 'runSugg_curVal':
            frMain =   TBS.Frame(parent)
            frMain.pack(fill='x',pady=5)
            strings = S.layout['run']['suggUI']['curValue']
            TBS.Label(frMain,text=strings['lbl']).pack(side='left')
            self.suggWidgets['curVal'] = TBS.Button(frMain,text=strings['btn'],bootstyle='warning-outline')
            self.suggWidgets['curVal'].pack(fill='x',side='right')
        elif type == 'runSuggVars':
            if hasattr(self,'frSuggVars'): self.frSuggVars.destroy()
            if len(params): # здесь params = список[{'val':,'btn':},...] предложений для исправления
                self.frSuggVars = TBS.Frame(parent)
                self.frSuggVars.pack     (fill='x')

                self.buildSeparator(self.frSuggVars)
                TBS.Label(self.frSuggVars,text=S.layout['run']['suggUI']['vars']).pack(fill='x')
                for item in params: TBS.Button(self.frSuggVars,
                                              text    = item['btn'],
                                              command = lambda s=item['val']:self.suggVarClicked(s),
                                              bootstyle='info-outline').pack(fill='x',pady=4)
        elif type == 'runSuggEntry':
            frMain = TBS.Frame (parent)
            frMain.pack      (fill='x')
            self.buildSeparator(frMain,pady=7)
            TBS.Label(frMain,text=S.layout['run']['suggUI']['lblEntry']).pack(fill='x')

            self.suggWidgets['entry']   = TBS.Entry(frMain)
            self.suggWidgets['entry'].pack(fill='x',pady=7)
            for key in ('<Key-Return>','<KP_Enter>'):
                self.suggWidgets['entry'].bind(key,lambda event:self.suggFinalClicked('ok'))

            self.buildFrame('runSugg_entryButtons',frMain)  # кнопки ОК и Отмена
            self.setSuggState(False)
        elif type == 'runSugg_entryButtons':
            frMain =   TBS.Frame(parent)
            frMain.pack(fill='x',pady=3)
            self.lblInvalidUD = TBS.Label(frMain,foreground=G.colors['red'])
            self.lblInvalidUD.pack(side='left')
            for key,cfg in S.layout['run']['suggUI']['buttons'].items():
                self.suggWidgets[key] = TBS.Button(frMain,
                                                  text      = cfg['text'],
                                                  command   = lambda key=key:self.suggFinalClicked(key),
                                                  bootstyle = cfg['style'])
                self.suggWidgets[key].pack(side='right',padx=cfg['padx'])
        elif type == 'finish':
            self.frSugg .destroy   ()
            strings = S.layout['run']
            self.suggLfl.configure(text=strings['lfl']['finished'],bootstyle='success')
            frMain      = TBS.Frame(self.suggLfl)
            frMain.pack(padx=5,pady=2)
            self.errLbl = TBS.Label(frMain,text=strings['finished']['title']+str(params))
            self.errLbl.pack(anchor='w',padx=6)
            self.buildFrame('finButtons',frMain)
        elif type == 'finButtons':
            frMain =   TBS.Frame(parent)
            frMain.pack(fill='x',pady=7)
            self.finBtns = {}
            for btnType,cfg in S.layout['run']['finished']['buttons'].items():
                self.finBtns[btnType] = TBS.Button(
                    frMain,
                    text      = cfg['text'],
                    command   = self.buildUI if btnType == 'exit' else self.app.errors.showNotepad,
                    bootstyle = cfg['style']
                    )
                self.finBtns[btnType].pack(side=cfg['side'],padx=5)

    def buildTabs(self,parent:TBS.Frame):
            tabs  = TBS.Notebook(parent)
            tabs.pack(fill='both',expand=True,padx=7,pady=5)
            for type in ('main','extra','script'): self.buildFrame('MLtab',tabs,type)
    def buildActionsCfgGroup(self,parent:TBS.Frame,type:str,group:str):
        SE   = 'suggestErrors'
        stng = 'capitalize:selected'
        cur  =  StringVar(value=G.config.get(stng))
        for param,strings in S.layout['actionsCfg'][group].items():
            if param != SE or SE in G.launchTypes[type]['getUserCfg']:
                if  type  == 'capitalize' and group != 'forAll':
                    widget = TBS.Radiobutton(parent,
                                             text      = strings['lbl'],
                                             value     = param,
                                             variable  = cur,
                                             command   = lambda p=param:G.config.set(stng,p))
                else:
                    sType  = type+':'+param # например, 'checkTitles:newSheet'
                    widget = TBS.Checkbutton(parent,
                                             text      = strings['lbl'],
                                             variable  = BooleanVar    (value=G.config.get(sType)),
                                             command   = lambda t=sType:self.switchBoolSetting(t),
                                             bootstyle = 'round-toggle')
                    ToolTip(widget,text=strings['tt'])
                widget.pack(padx=5,pady=5,expand=True,anchor='w')
    def buildOnLaunchInputs (self,parent:TBS.Frame,type:str,inputs:list):
        self.onLaunch = {}
        for param in inputs:
            frame = TBS.Frame(parent)
            frame.pack(fill='x',pady=3)
            TBS.Label(frame,text =   S.layout['getOnLaunch'][type][param]).pack(side='left',padx=2)
            self.onLaunch[param] = TBS.Entry(frame)
            self.onLaunch[param].insert(0,str(G.config.get(type+':'+param)))
            self.onLaunch[param].pack(fill='x',expand=True,side='right',padx=5)
    def buildSeparator(self,parent,padx=0,pady=3): TBS.Separator(parent).pack(fill='x',padx=padx,pady=pady)

    # вспомогательные
    def log(self,string:str,unit:str):
        try   : color = G.colors[G.log['colors'][unit]]
        except: color = None
        TBS.Label(self.frLog,text=string,foreground=color).pack(fill='x')
    def loadExcelList (self):
        G.exBooks.update()
        if G.exBooks.cur:   # Excel открыт, и не только стартовый экран
            self.fileList.configure(values=G.exBooks.bookNames,state='readonly')
            self.fileList.set      (G.exBooks.cur)
        else:
            self.fileList.set      (S.layout['main']['msg']['noFilesFound'])
            self.fileList.configure(state='disabled')
        if self.frRight is not None: self.setLaunchBtnState()
    def setSuggTitle(self,errorsLeft=0):
        strings = S.layout ['run']['suggUI']['errorsLeft']
        if errorsLeft == 1: count = strings['one']
        else:               count = strings['many'].replace('$$2',str(errorsLeft))
        self.lblSuggType.configure(text=S.suggMsg[self.curError.type]+count)
    def setSuggState(self,enabled:bool):
        if  hasattr  (self,'frSuggVars'): self.frSuggVars.destroy()
        for widget in self.suggWidgets.values(): widget.configure(state=('disabled','normal')[enabled])
        if not enabled: self.lblSuggType.configure(text='')
    def setSuggErrorState(self,error:bool,vObj=None):   # vObj={'type':,'value':,'valid':,'errKey':}
        self.lblInvalidUD.configure(text = S.errInput[vObj['type']][vObj['errKey']] if error else '')
    def suggInvalidUD(self,errObj,suggList:list,errorsLeft:int):
        self.curError = errObj
        self.setSuggTitle(errorsLeft)
        self.setSuggState(True)
        self.suggWidgets ['curVal'].configure(text=errObj.initVal,command=lambda s=errObj.initVal:self.suggVarClicked(s))
        self.buildFrame  ('runSuggVars',self.frSuggMain,suggList)
        self.suggVarClicked(errObj.initVal) # добавляем в entry текущее значение
    def finish(self,errorsCount:int): self.buildFrame('finish',self.suggLfl,errorsCount)
    def launchErr(self,type:str):
        # если запущено с ошибкой, показывает её и завершает выполнение
        strings = S.layout['run']
        self.finish(1)
        self.suggLfl        .configure(text=strings['lfl']  ['launchErr'],bootstyle='danger')
        self.errLbl         .configure(text=strings['finished']['errors'][type])
        self.finBtns['exit'].configure(bootstyle='danger')

    # кнопки и переключатели
    def switchBoolSetting(self,param:str):
        newVal = not G.config.get(param)
        G.config.set(param,newVal)
        if param == 'main:darkTheme':
            self.style.theme_use(G.app['themes'][newVal])
            G.colors           = G.themeColors  [newVal]
            G.colors     .update(G.exColors)
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
            for param in G.launchTypes[type]['getOnLaunch']:
                G.config.set(type+':'+param,self.onLaunch[param].get())
            self   .buildUI(True)
            self.app.launch(book,type)
    def suggVarClicked(self,value):
        self.suggWidgets['entry'].delete(0,TBS.END)
        self.suggWidgets['entry'].insert(0,value)
        self.setSuggErrorState(False)
    def suggFinalClicked(self,btn:str):       # btn = либо 'ok', либо 'cancel'
        self.setSuggErrorState (False)
        if btn == 'ok':
            VAL =      self.app.validate_andCapitalize(self.curError.type,self.suggWidgets['entry'].get())
            if VAL['valid']: self.app.suggFinalClicked(True,VAL['value'])
            else:            self   .setSuggErrorState(True,VAL)
        else:                self.app.suggFinalClicked(False)
class Errors(): # фрейм ошибок
    def __init__(self,parent:TBS.Labelframe):
        self.storage = {}                   # {type:{initLow:TBS.Label,...},...}
        self.frame   = TBS.Frame(parent)    # внутренний фрейм с нужными отступами
        self.frame.pack(fill='both',expand=True,padx=10,pady=5)
    def add(self,type:str,low:str,text:str):
        if type not in self.storage.keys(): self.storage[type] = {}
        self.storage[type][low] = TBS.Label(self.frame,text=text)
        self.storage[type][low].pack(fill='x')
    def rm(self,errObj):    # ErrorObj() из модуля rootClasses
        self.storage[errObj.type].pop(errObj.initVal.lower()).destroy() # .pop() удаляет ключ и возвращает значение

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
