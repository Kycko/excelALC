from   sys                          import exit as SYSEXIT
import ttkbootstrap                     as TBS
from   ttkbootstrap.dialogs.dialogs import Messagebox
import globalsMain                      as G
import strings                          as S
import dictFuncs                        as dictF

def cantReadLib(): Messagebox.ok(S.layout['main']['msg']['cantReadLib'],G.UI.app['title'])

class Window(TBS.Window):   # окно программы
    # конструкторы интерфейса
    def __init__  (self,app):
        self.app = app  # для вызова функций класса Root() при нажатии кнопок
        super().__init__(title     = G.UI.app['title'],
                         themename = G.UI.app['themes'][G.config.get('main:darkTheme')],
                         size      = G.UI.app['size'],
                         minsize   = G.UI.app['size'])
        self.bindSpace()
        self.place_window_center()  # расположить в центре экрана
        self.buildUI()
    def bindSpace (self):
        def callDefault(event):
            try:
                widget = self.nametowidget(event.widget)
                widget.invoke()
            except KeyError: self.tk.call(event.widget,'invoke')

        self.bind_class('TButton','<Key-space>',callDefault,add='+')
    def buildUI   (self,runUI=False):   # runUI = окно выбора (False) или окно выполнения (True)
        if hasattr(self,'frRoot'): self.frRoot.destroy()
        self.frRight = None # сначала это: он читается в self.loadExcelList()
        self.frRoot  = TBS.Frame(self)
        self.frRoot.pack(fill='both',expand=True,padx=10,pady=10)
        self.buildFrame (('mainLeft','mainRun')[runUI],self.frRoot)
    def buildFrame(self,type:str,parent,params=None):
        # frMain = TBS.Frame либо TBS.Labelframe

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
