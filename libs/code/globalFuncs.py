from sys import exit as SYSEXIT

def getIB(type, index): # IB = index/boolean
    # служебная функция, которая возвращает либо сам index, либо true/false в зависимости от значения index
    return index if type == 'index' else index >= 0

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
