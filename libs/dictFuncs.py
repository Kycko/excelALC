from sys import exit as SYSEXIT

def update(dict:dict,root:dict=None,inner:dict=None):
  # добавляет всё из root в корень dict, а inner рекурсивно, чтобы не затирать данные
  # ключи в inner должны содержать пути через ':' (либо единственный ключ)
  if root  is not None: dict.update(root)
  if inner is not None:
    for keys,new in inner.items():
      cur = dict
      for key in keys.split(':'): cur = cur[key]
      cur.update(new)
  return dict

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
