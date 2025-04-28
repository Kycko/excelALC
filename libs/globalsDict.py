from sys import exit as SYSEXIT

class globDicts():  # импортируется в G.dict (в глобальные переменные)
  def __init__(self):
    pass

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
