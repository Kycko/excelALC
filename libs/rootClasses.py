from   sys import exit as SYSEXIT
import libClasses      as lib

# корневой класс: из него запускаются UI и код других модулей
class Root():
    def __init__(self):
        if lib.ready:

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
