# можно использовать в других программах
from   sys import exit as SYSEXIT
import globalFuncs     as GF

class userCfg():
    def __init__(self,file:str):
        def _init():
            self.storage = GF.get_initSettings()    # self.storage – основное хранилище всех настроек
            self.write()

        self.file = file
        try   : self.read()
        except:     _init()
    def get  (self,param:str):
        # для упрощения кода в param педедаём section:key с разделителем
        section,key = param.split(':')
        try:    return self.storage[section][key]
        except: return True
    def set  (self,param:str,value,saveFile=True):
        # для упрощения кода в param педедаём section:key с разделителем
        section,key = param.split(':')
        if section not in self.storage.keys(): self.storage[section] = {}
        self.storage[section][key] = value
        if saveFile: self.write()
    def read (self):
        def toStorage(list:list):
            self.storage = {}
            for line in list:
                param,  value = line.split(' ',1)
                try   : value = int(value)
                except:
                    if value in ('True','False'): value = value == 'True'
                self.set(param,value,False)
        toStorage    (GF.readFile(self.file))
    def write(self):
        def parseStorage():
            final = []
            for section,paramDict in self.storage.items():
                for key,value     in paramDict   .items():
                    final.append(section+':'+key+' '+str(value))
            return final
        GF.write_toFile (parseStorage(),self.file)

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
