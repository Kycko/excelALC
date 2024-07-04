from sys   import exit as SYSEXIT
from appUI import Window
# корневой класс: из него запускаются UI и код других модулей
class Root():
    def __init__(self):
        self.UI = Window()
        self.UI.mainloop()

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
