from sys import exit as SYSEXIT

class globDicts():  # импортируется в G.dict (в глобальные переменные)
  def __init__(self):
    # эти свойства записываются в rootClasses.pr{} (properties)
    self.tasks = {'chkCat':{'read'        : 'selection',
                            'toTD'        :  False,
                            'addHeader'   :  False,
                            'launch'      : 'rangeChecker',
                            'justVerify'  :  False,
                            'resetBg'     : 'selection',
                            'hlTitles'    :  False,
                            'AStype'      : 'cat',
                            'cfg'         :('newSheet',
                                            'suggErrors',
                                            'saveAfter')},
                  'chkSrc':{'read'        : 'selection',
                            'toTD'        :  False,
                            'addHeader'   :  False,
                            'launch'      : 'rangeChecker',
                            'justVerify'  :  False,
                            'resetBg'     : 'selection',
                            'hlTitles'    :  False,
                            'AStype'      : 'source',
                            'cfg'         :('newSheet',
                                            'suggErrors',
                                            'saveAfter')}}

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
