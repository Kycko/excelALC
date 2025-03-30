from sys import exit as SYSEXIT

class globUI(): # импортируется в G.UI (в глобальные переменные)
    def __init__(self):
        # базовые переменные приложения
        self.app = {'version':'v.103',
                    'name'   :'excelALC'}
        self.app   ['title'] = self.app['name']+' '+self.app['version'] # название главного окна

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
