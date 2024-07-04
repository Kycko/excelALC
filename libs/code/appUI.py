from   sys          import exit as SYSEXIT
import ttkbootstrap             as TBS
from   ttkbootstrap.tooltip import ToolTip
import globalVars               as G
import strings                  as S

# шаблоны моих классов (B=button)
class Btemplate(TBS.Button):
    def __init__(self,master,text=None,image=None,width=None,bootstyle='primary',command=None):
        super().__init__(master=master,command=command,text=text,image=image,width=width,bootstyle=bootstyle)
        self   .bind    ('<KeyPress-Return>',  command) # обрабатывает оба Enter'а (+numpad)
        self   .bind    ('<KeyPress-space>',   command)

# окно программы
class Window(TBS.Window):
    def __init__(self):
        super().__init__(title     = G.app['TV'],
                         themename = G.app['themes'][G.config.get('main:darkTheme')],
                         size      = G.app['size'],
                         minsize   = G.app['size'])
        self.place_window_center()  # расположить в центре экрана
        self.buildInitUI()
    def buildInitUI(self):
        self.frRoot = TBS.Frame(self)
        self.buildFrame('left')
    def buildFrame(self,type:str):
        if type == 'left':
            frLeft = TBS.Frame(self.frRoot) # основной фрейм
            self.buildFrFile  (frLeft)
            tabs   = TBS .Notebook   (frLeft)
            frDown = TBS .Frame      (frLeft)
            tabs  .pack(fill='x',       padx=7,pady=2)
            frDown.pack(fill='x',side='bottom',pady=5)
    def buildFrFile(self,parent:TBS.Frame):
        frMain        = TBS.Frame   (parent)
        lbl           = TBS.Label   (frMain,text =S.layout['main']['lbl']['selectFile'])
        self.fileList = TBS.Combobox(frMain,width=33,bootstyle='success')

        pic           = TBS.PhotoImage(file=G.pics['filesUpdate'])
        btn           = Btemplate(self,image=pic,command=self.loadExcelList,bootstyle='link')
        btn.image     = pic # баг tkinter'a, нужно указать повторно
        ToolTip(btn,text=S.layout['main']['tt']['filesUpdate'])

        frMain       .pack(fill='x'   ,pady=2)
        lbl          .pack(side='left',padx=8)
        btn          .pack(side='right')
        self.fileList.pack(pady=5)
        self    .loadExcelList()
        self.fileList.focus_set()
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

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
