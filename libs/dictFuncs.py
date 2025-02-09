from sys import exit as SYSEXIT

def getByPath(dict:dict,path:str):
    # возвращает значение словаря, записанное по пути path
    # элементы path должны быть разделены двоеточиями; path может иметь любую длину
    # например, если path='tasks:main:lbl', функция вернёт значение dict['tasks']['main']['lbl']
    path  = path.split(':')
    final = dict[path[0]]
    for key in path[1:]: final = final[key]
    return final

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
