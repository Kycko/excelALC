from   sys import exit as SYSEXIT
import ttkbootstrap    as TBS
import globalVars      as G

# окно программы
class Window(TBS.Window):
    def __init__(self):
        super().__init__(title=G.app['TV'], themename=G.app['themes'][G.config.get('main:darkTheme')])
        self.setGeometry()
        self.buildFrames()

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
