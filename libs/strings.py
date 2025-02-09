from sys        import exit  as SYSEXIT
from globalsMain import files as gFiles

cantReadLib = 'Ошибка чтения файла "'+gFiles['lib']+'". Программа не может быть запущена.'

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
