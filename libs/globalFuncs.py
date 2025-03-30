from sys import exit as SYSEXIT

# системные
def sysExit(self=None): SYSEXIT()   # self для привязки к нажатию кнопок

# глобальные
def readFile(file:str):
    with open(file,'r',encoding='utf-8') as f: return [line.strip() for line in f]
def write_toFile(list:list,file:str,justAdd=False):
    # если justAdd=True, предыдущие данные останутся в файле
    if justAdd: mode,list = 'a',[list]
    else:       mode      = 'w'

    with open(file,mode,encoding='utf-8') as f:
        for line in list: f.write(f"{line}\n")
def get_initSettings(): return {'main':{'darkTheme':checkWinTheme(),
                                        'zoom'     :0}}

# GUI
def checkWinTheme(): 
    try:                import winreg
    except ImportError: return True

    registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    keyPath  = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:                      regKey = winreg.OpenKey(registry,keyPath)
    except FileNotFoundError: return True

    for i in range(1024):
        try:
            valueName,value, _ = winreg.EnumValue(regKey, i)
            if valueName == 'AppsUseLightTheme': return bool(1-value)   # инвертируем 0 и 1
        except OSError: break
    return True

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
