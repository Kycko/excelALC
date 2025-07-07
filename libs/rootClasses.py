from   sys               import exit as SYSEXIT
from   xlwings.constants import HAlign
from   copy              import deepcopy
from   globalFuncs       import curDateTime,write_toFile
import globalsMain           as G
import appUI
from   excelRW           import Excel
from   tables            import Table,CellTable,TableDict
import strings               as  S
import stringFuncs           as  strF
import listFuncs             as listF
import libClasses            as lib

# корневой класс: из него запускаются UI и код других модулей
class Root():
  def __init__(self):
    if lib.ready:
      self.UI = appUI.Window(self)
      self.UI.mainloop()
    else: appUI.cantReadLib()
  def launch  (self,book,type:str):
    # book = {obj:,file:,sheet:}; type = например, 'chkCat'
    def _getCfg ():
      self.cfg = {p:G.config.get(type+':'+p) for p in self.pr['cfg'] if p != '---'}
      try:
        for key,val in self.pr['forceCfg'].items(): self.cfg[key] = val
      except: pass
    def _initLE (): # LE = log & errors
      self.log = Log(self.UI)
      initStr  = self.log.add('mainLaunch',{'time':curDateTime(),'file':book['file']})
      self.log.add           ('launchType',{'str' :S.UI['tasks'][type]['log']})
      self.errors = Errors(self.log,self.UI,initStr)
    def _getData(logging=True,rmRC=False):
      def _getLog():
        rng  = ('range','full')[self.pr['read'] == 'shActive']
        type = 'readRange:'+rng

        rpl = {'addr':tObj['addr']}
        c   =     len(tObj['table'].data[0])
        r   =     len(tObj['table'].data) - 1*(rng == 'full') # без заголовка
        rpl['cols'] = str(c)+' '+S.wordEndings['столбцы'][strF.ending_byCount(c)]
        rpl['rows'] = str(r)+' '+S.wordEndings['строки' ][strF.ending_byCount(r)]
        return type,rpl
      def _curTD ():
        uTD,self.curTD = self.unkTD,TableDict()
        for lKey,par in lib.columns.data.items():
          uKey = uTD.searchTitle(par['title'])
          if uKey is not None:
            uTD.columns[uKey].title.value = par['title']  # для правильной капитализации
            self.moveUnkTD_toCurTD(uKey,lKey)

      self.file = Excel(book['obj'],self.pr['read'],('toStrings'))
      for shName,tObj in self.file.data.items():
        # for выполнится один раз; обращение через .keys()[0] и .values()[0] не работает
        self.shName = shName
        if self.pr['read'] == 'shActive':
          tObj['table'].cutUp(self.searchTitleRow(tObj['table']))
        if logging:
          self.log.add('readSheet',{'sheet':shName})  # имя листа
          self.log.add(*_getLog())                    # диапазон

        if self.pr['toTD']:
          self.unkTD = TableDict(tObj['table'])
          if rmRC: self.rmRC_initial(self.unkTD)
          _curTD()
        else: self.table = CellTable(tObj['table'])
    def _runType():
      def    _runRange(type:str):
        if type == 'title': data = [[col.title for col in self.unkTD.columns.values()]]
        else              : data =  self.table.data
        self.rangeChecker(data,type)
      def    _runVerts():
        def _vertUpdData():
          # возвращает Table из тех же строк столбца с заголовком 'Категория'
          # + обновляет self.file по selection'у
          catIndex = self.searchTitleCol(lib.columns.data['cat']['title'])
          if len(catIndex) == 1:
            range           =  self.file.data[self.shName]['range']
            cats            =  self.file.getValues(range.offset(0,catIndex[0]+1-range.column))
            self.pr['read'] = 'selection'
            _getData(False)
            return CellTable(Table(cats,('toStrings')))
        if self.file.data[self.shName]['range'].columns.count != 1: self.UI.launchErr('oneCol')
        else:
          cats = _vertUpdData()
          if cats is None: self.UI.launchErr('noCats')
          else           :  self.vertChecker(self.table.data,cats.data)
      def  _fillBlanks():
        count = 0
        for   row  in self.table.data:
          for cell in row:
            if not cell.value.replace(' ',' ').strip():
              cell.value = self.cfg['strFiller']
              count     += 1
        self.log.add('blanksFilled',{'count':count})
        self. finish()
      def  _capitalize():
        mask = self.cfg['captMask']
        for   row  in self.table.data:
          for cell in row:
            new = strF.capitalize(cell.value,mask)
            if new != cell.value:
              self.log.add('ACsuccess',{'type':mask,'from':cell.value,'to':new})
            cell.value = new
        self.finish()
      def _formatSheet():
        def _check():
          for  key,val in self.cfg.items():
            if key != 'frmRange' and key[:3] == 'frm' and val: return True
          return False
        if  _check():
          self.log.add('frmSelRange' if [self.cfg['frmRange']] else 'frmSelSheet')
          self.finish(self.cfg['newSheet'])
        else        : self.UI.launchErr   ('noOpts')

      match self.pr['launch']:
        case 'capitalize' :       _capitalize()
        case 'chkAll'     :         _runRange('title')
        case 'chkRange'   :         _runRange(self.pr['AStype'])
        case 'chkVerts'   :         _runVerts()
        case 'fillBlanks' :       _fillBlanks()
        case 'formatSheet':      _formatSheet()
        case 'rmRC'       : self.rmRC_initial(self.table); self.finish()

    self.type   = type
    self.pr     = deepcopy(G.dict.tasks[type])  # некоторые параметры меняются в процессе
    self.stages = None  # всегда сбрасываем для правильной работы chkAll

    _getCfg ()
    _initLE ()  # LE = log & errors
    _getData(rmRC=self.pr['rmRC_onRead'])
    _runType()

  # основные алгоритмы проверки
  def rangeChecker(self,table :list,type :str):
    # в table передаём либо CellTable().data, либо [cells[]] из TableColumn
    # т. е. table – это всегда [[Cell,...],...]
    def _addError(): errors[low] = ErrorObj(type,cell.value,errPos)

    self.rTable  = table  # range table, понадобится в self.finalizeErrors()
    errors,fixed = {},{}  # {initLow:ErrorObj,...}, {fromLow:to,...}
    for   r in range(len(table)):
      for c in range(len(table[r])):
        cell   =   table[r][c]
        errPos = {'r':r,'c':c}

        low   = cell.value.lower()
        try   : cell.value = fixed[low]
        except:
          try   : errors[low].addPos(errPos)
          except:
            JV      = self.pr['justVerify']
            tempVal = cell.value
            VAL     = self.validate_andCapitalize(type,tempVal)
            if not VAL['valid'] and not JV:
              tempVal = self.autocorr(type,tempVal)
              VAL     = self.validate_andCapitalize(type,tempVal)

            if   VAL['valid']:
              if VAL['value'] != cell.value:  # иначе ничего делать не надо (ошибки нет)
                if JV: _addError()
                else: # это только про autocorr?
                  self.log.add('ACsuccess',{'type':type,'from':cell.value,'to':VAL['value']})
                  fixed[low] = VAL['value']
                  cell.value = VAL['value']
            else: _addError()

    self.errors.addCur(errors)
    self.nextSugg()
  def  vertChecker(self,tVerts:list,tCats:list):
    # в tVerts/tCats передаём либо CellTable().data, либо [cells[]] из TableColumn: это всегда [[Cell,...],...]
    def _double  ():
      def _copy():
        fRow,fCol  = err.pos[0]['r'],err.pos[0]['c']
        VC.value   = tVerts[fRow][fCol].value
        VC.error   = tVerts[fRow][fCol].error
        VC.changed = tVerts[fRow][fCol].changed
      err = errors[CVlow]
      err .addPos(errPos)
      _copy()
    def _addError():
      errors[CVlow] = ErrorObj('vert',CVstr,errPos)
      VC.error      = True
    def _log     ():
      if CVstr not in AClogger:
        AClogger.append( CVstr)
        self.log.add   ('ACsuccess',{'type':'vert','from':CVstr,'to':new})

    AClogger     = []     # запоминаем autocorr'ы для журнала (например, Services -> Услуги)
    errors       = {}     # {initLow:ErrorObj,...}
    vertsChanged = False  # чтобы показать сообщение про changed только один раз
    self.rTable = tVerts  # range table, понадобится в self.finalizeErrors()

    for   r in range(len(tVerts)):
      for c in range(len(tVerts[r])):
        VC       = tVerts[r][c] # это vert cell (CellObj)
        stripped = VC.value.replace(' ',' ').strip()
        if not self.cfg['vertBlanks'] or not stripped:
          lowCat = tCats [r][c].value.lower()         #  это string
          CVstr  = tCats [r][c].value+' | '+VC.value  # 'cat | vert'
          CVlib  = lib.cat.catVertList                #  cat & vert
          errPos = {'r':r,'c':c}
          new    = CVlib[lowCat] if lowCat in CVlib.keys() else ''

          CVlow     = CVstr.lower()
          if CVlow in errors.keys(): _double()
          else:
            if self.pr['justVerify'] or not self.cfg['ACverts']:
              if new != VC.value: _addError()
            else:
              ACval = self.autocorr('vert',VC.value)
              if new:
                if VC.value  !=   new: _log()
                if stripped and ACval.lower() != new.lower():
                  vertsChanged,VC.changed = True,True
              else  : _addError()
              VC.value = new

    if vertsChanged: self.log.add('vertChanged')
    self.errors.addCur(errors)
    self     .nextSugg()
  def rmRC_initial(self,tObj):  # удаляет только в ОЗУ; потом ещё надо удалить в файле
    # tObj = CellTable либо TableDict
    def _log():
      RC  = {'rows':len(self.RCremoved['rows']),
             'cols':len(self.RCremoved['cols'])}
      key = 'RAM' if RC['rows'] or RC['cols'] else 'NO'
      self.log.add('RCremoved_'+key,RC)
    self.RCremoved = tObj.rmEmptyRC('rc',self.cfg['rmTitledCols'])
    _log()
  def nextStage   (self):
    # запускает проверку следующего столбца для 'allChecks'
    def _log(key:str,type:str=None):
      if self.type == 'chkAll': # чтобы не выводить для reCalc
        t = None if type is None else S.AStypes[type]
        self.log.add(key,{'col':curCol.title.value,'type':t})

    cols = self.curTD.columns
    if self.stages is None: self.stages = list(cols.keys())
    if self.stages:
      try:
        kk = 'cat'
        self.stages.remove(kk)  # возникнет ValueError, если такого в списке нет
      except: kk = self.stages.pop(0)

      curCol = cols[kk]
      temp   = curCol.type.split(':')
      type   = temp.pop(0)
      if len(temp): self.subtype = temp[0]

      if    type == 'vert':
        if 'cat' in cols.keys():
          _log('stg+',type)
          self.vertChecker([curCol.cells],[cols['cat'].cells])
        else:  _log('stgVert-')
      elif  type in  G.dict.AStypes.keys():
        _log('stg+',type)
        self.rangeChecker([curCol.cells],type)
      else: _log('stg-'); self.nextStage()
    else: self.finish()

  # работа с ошибками
  def autocorr(self,type:str,value:str):
    def _getAC(): return lib.autocorr.get(type,value)

    value    =  strF.autocorrCell(type,value,self.cfg)
    if type == 'region':
      AC     = _getAC() # сперва в autocorr без изменений, потом после них
      if AC['fixed']: return AC['value']
      else          : value = strF.ACcity(value,
                                          lib.regions,
                                          lib.autocorr,
                                          self.cfg['forceDblRegions'])

    AC = _getAC()
    return AC['value']
  def validate_andCapitalize(self,type:str,value:str,extra=None):
    # в extra можно передать любые необходимые доп. данные
    params = G.dict.AStypes[type]
    # ↓ передаём в extra suggList из appUI.suggInvalidUD()
    if extra is None and params['readLib']: extra = lib.get_vList(type)
    final = {'type'  :type,
             'value' :value,
             'valid' :None,
             'errKey':''} # ключ сообщения для suggUI

    if params['checkList']:
      found          = listF.searchStr(extra,value,'item',True,not self.pr['justVerify'])
      final['valid'] = bool(found)
      if final['valid']:
        if not self.pr['justVerify']: final['value'] = found[0]
      else: final['errKey'] = 'notInList'
    else: strF.validateCell(final,self.cfg) # final обновляется внутри
    return final
  def nextSugg(self):
    def _getSuggList(errObj):
      type,val = errObj.type,errObj.initVal
      if AST[type]['getLibSugg']: return lib .sugg   .get(type,val)
      else:                       return strF.getSuggList(type,val)

    queue = self.errors.queue
    JV    = self.pr['justVerify']
    AST   = G.dict.AStypes
    if JV or not self.cfg['suggErrors']:
      # после этого выполняется elif ниже
      for i in range(len(queue)): self.errors.suggClicked(False,'',True)
    if queue and AST[queue[0].type]['showSugg']:
      self.UI.suggInvalidUD(queue,_getSuggList(queue[0])[:9])
    else: self.finalizeErrors()
  def suggFinalClicked(self,OKclicked:bool,newValue=''):
    self.errors.suggClicked(OKclicked,newValue)
    self.nextSugg()
  def   finalizeErrors(self):
    def _processQueue ():
      for lng in range(len(self.errors.qStage)):
        errObj = self.errors.qStage.pop(0)
        for i in range(len(errObj.pos)):
          # self.rTable – это всегда [[Cell,...],...]
          errPos = errObj.pos[i]
          cell   = self.rTable[errPos['r']][errPos['c']]
          if errObj.type == 'title' and i: cell.error = True
          else:
            cell.error = not errObj.fixed
            if errObj.fixed: cell.value = errObj.newVal
        self.errors.qFinal.append(errObj)
    def _titles       ():
      def _fixed(): # сперва переносим исправленные
        keys = [] # ключи[(unkKey,curKey),...] для перемещения из unkTD в curTD
        for uKey,col in self.unkTD.columns.items():
          if not col.title.error:
            keys.append((uKey,cLib.getKey_byTitle(col.title.value)))
        for item in keys:  self.moveUnkTD_toCurTD(*item)
      def _add  (): # затем  добавляем обязательные
        cnt,cTD = 10000,self.curTD
        rows    = len(tuple(cTD.columns.values())[0].cells)
        for key,params in cLib.data.items():
          if params['mandatory'] and key not in cTD.columns.keys():
            cTD .addEmptyColumn(key,params['title'],rows,cLib.data[key]['type'])
            cTD .columns[key].initPos = cnt; cnt += 1
            self.log.add('+column',{'title':params['title']})
      if self.type == 'chkTitles' or (self.type == 'chkAll' and self.stages is None):
        cLib = lib.columns
        _fixed(); _add()

    _processQueue()
    if self.pr['read'] == 'selection'  : self.table.data = self.rTable
    else                               : _titles()  # проверки внутри
    if self.type in ('chkAll','reCalc'): self.nextStage()
    else                               : self.finish()

  # чтение данных из таблицы
  def searchTitleRow   (self,table :Table):
    for  r   in range(len(table.data)):
      if strF.findSubList(table.data[r][0],('Уникальных: ','Ошибок: '),'index') != 0: return r
    return 0
  def searchTitleCol   (self,title :str):
    # возвращает индексЫ (список[]) столбцов с заголовком title, отсекая шапку (errors/unique)
    rawTable = self.file.data[self.shName]['table']
    titleRow = rawTable .data[self.searchTitleRow(rawTable)]
    return listF.searchStr(titleRow,title,'index',True,False)
  def moveUnkTD_toCurTD(self,unkKey:str,curKey:str):
    curCols,cLib    = self.curTD.columns,lib.columns.data
    curCols[curKey] = self.unkTD.columns.pop(unkKey)
    curCols[curKey].type = cLib[curKey]['type'] if curKey in cLib.keys() else None

  # финальные шаги (преобразование и запись)
  def finish(self,forceNewSheet=False):
    def _TDjoin():  # объединяем curTD и unkTD перед финальной записью
      for key in tuple(self.unkTD.columns.keys()): self.moveUnkTD_toCurTD(key,key)
    def _curTD_toTable():
      def _reorder(): # изменяет в столбцах initPos: по нему будет расстановка при записи
        def _byLib(): # сперва из библиотеки
          counter   = 0
          for  key in libData.keys():
            if key in keys:
              keys.remove(key)
              cTD.columns[key].initPos = counter
              counter += 1
          return counter
        def _unk  (counter:int):  # затем с неправильными названиями
          for i in sorted([int(key) for key in keys]):
            cTD.columns[str(i)].initPos = counter
            counter += 1
        keys = list(cTD.columns.keys())
        _unk(_byLib())
        self.log.add('titlesReordered')
      cTD,libData = self.curTD,lib.columns.data
      if self.cfg['reorder']: _reorder()
      self.table = cTD.toCellTable(self.pr['addHeader'],libData,S.tblHeader)
    def   _write():
      def _copySheet():
        def _rng(): shObj['range'] = shObj['sheet'].range(shObj['addr'])
        self.file.copySheet(self.shName)
        match self.pr['read']:
          case 'selection'  : _rng()
          case 'shSelection': _rng()
          case 'shActive'   :
            rows  = len(shObj['table'].data)
            cols  = len(shObj['table'].data[0])
            shObj['range'] = shObj['sheet'].range((1,1),(rows,cols))
            shObj['addr']  = shObj['range'].address
            shObj['sheet'].clear_contents()
      def _rmRC():
        try:
          RC  = self.RCremoved
          r,c = len(RC['rows']),len(RC['cols'])
          for RCkey  in RC.keys (): RC[RCkey] = listF.ints_toRanges(RC[RCkey],True)
          for rc,lst in RC.items():
            for rng in lst: self.file.rmRCrange(self.shName,rc,rng)
          if r or c: self.log.add('RCremoved_file',{'rows':r,'cols':c})
        except: pass

      newSheet  = G.config.get(self.type+':newSheet')
      shObj     = self.file.data[self.shName]
      self.tObj = self.table.toTable()
      equal     = self.tObj. equals (shObj['table'])

      if not equal:
        shObj['table'] = self.tObj
        if newSheet: _copySheet()
        _rmRC()
        if self.pr['read'] == 'shActive': self.file.clearData(self.shName)
        self.file.write(self.shName)
      elif forceNewSheet: _copySheet()

      if self.type == 'formatSheet': equal = False
      self.log.add('finalWrite'+'+-'[equal],{'sheet':S.log['FWvars'][newSheet]})
    def  _format(forceFrm:bool):  # forceFrm, вроде, исп. только для chkAll
      def _set(type:str=None,force=False):
        def _unPin   (): self.file.callPin(False)
        def _unFilter(): self.file. filter(False,frmSheet['sheet'])

        cRng = self.cfg['frmRange']

        if force or type ==  'frmResetAll' :
          fRange.clear_formats(); _unPin(); _unFilter()
          self.log.add('frmResetAll')
        elif    not self.cfg['frmResetAll']:
          if type == 'frmBorders' :
            fRange.api.Borders.Weight = 2
            fRange.api.Borders.Color  = clrs['borders']
            self.log.add(type)
          if type == 'frmBg'      :
            fRange.color = None
            self.log.add(type)
          if type == 'frmFg'      :
            RF.color = clrs['blackFont']
            self.log.add(type)
          if type == 'frmBIU'     :
            RF.bold   = False
            RF.italic = False
            fRange.api.Font.Underline = -4142 # так отключается подчёркивание
            self.log.add(type)
          if type == 'frmFont'    :
            RF.name = glob['font']['name']
            RF.size = glob['font']['size']
            self.log.add(type)
          if type == 'frmAlign'   :
            fRange.api.HorizontalAlignment = HAlign.xlHAlignLeft
            self.log.add(type)
          if type == 'frmNewLines':
            fRange.api.WrapText = False
            self.log.add(type)
          if type == 'frmUnPin'    and not cRng:
            _unPin()
            self.log.add(type)
          if type == 'frmUnFilter' and not cRng:
            _unFilter()
            self.log.add(type)

        if force or (type == 'frmPinTitle' and not cRng):
          self.file.pinTitle(self.shName,tRow)
          self.log.add('frmPinTitle')
        if force or (type == 'frmFilter'   and not cRng):
          self.file.filter(True,frmSheet['sheet'].range((tRow+1,1),self.tObj.getSize()))
          self.log.add('frmFilter')

      glob     = G.dict.frmExcel
      clrs     = G.dict.exColors
      frmSheet = self.file.data[self.shName]
      fRange   = frmSheet['range'] if self.cfg['frmRange'] else frmSheet['sheet'].cells
      RF       = fRange.font  # RF = range font

      if forceFrm: _set(force=True)
      else:
        for key,val in self.cfg.items():
          if key != 'frmRange' and key[:3] == 'frm' and val: _set(type=key)
    def  _colors():
      # шапку подсвечиваем в любом случае
      def _hlRow(r:int,type:str):
        def _set(colorKey:str):
            self.file.setCellColor(self.shName,
                                   self.pr['read'],
                                   r,c,
                                   G.dict.exColors[colorKey])
        for c in range(len(tbl[r])):
          err,chg = tbl[r][c].error,tbl[r][c].changed
          if   type == 'errors'     and     err: _set('hlError')
          elif type == 'chVerts'    and     chg: _set('hlChanged')
          elif type == 'goodTitles' and not err: _set('goodTitle')
      def _log  ():
        if not totalErrors      : key = '0'
        elif   totalErrors < 501: key = 'done'
        else                    : key = 'skip'
        if resBg != 'none': self.log.add('finalColors_'+key,{'count':str(totalErrors)})

      resBg = self.pr['colors'].split(':')[0]
      self.file.resetBgColors(self.shName,resBg)
      tbl = self.table.data
      if totalErrors in range(1,501): last =  len (tbl)
      else:                           last = (0,2)[self.pr['addHeader']]
      for row in range(last): _hlRow(row,'errors')

      if 'tit'  in self.pr['colors']: _hlRow(tRow,'goodTitles')
      if 'vert' in self.pr['colors']:
        for row in range  (len(tbl)): _hlRow(row,'chVerts') # changed verticals
      _log()

    totalErrors = self.errors.getCount()
    if self.pr['toTD']: _TDjoin(); _curTD_toTable()
    _write()
    tRow = self.searchTitleRow(self.tObj)
    if 'frm' in self.pr['colors'] and self.cfg['formatSheet']:
      _format(self.type == 'chkAll')
    _colors()
    if G.config.get(self.type+':saveAfter'):
      self.file.save()
      self.log .add ('fileSaved')
    self.UI .finish(totalErrors)

# журнал и ошибки
class Log     (): # журнал
  def __init__(self,UI:appUI.Window):
    self.UI   = UI
    self.file = G.files['log']
    write_toFile([],self.file)
  def add(self,type:str,rpl:dict=None):
    # rpl=replace (словарь строк для замены переменных)
    def _getType():
      unit,txt = G.dict.log[type],S.log[type]
      if rpl is not None: txt = strF.replaceVars(txt,rpl)
      return '['+unit+'] ' + txt,unit
    newStr,unit = _getType()
    write_toFile(newStr,self.file,True)
    self.UI.log (newStr,unit)
    return newStr # пока что нужно только для _initLE()
class Errors  (): # хранилище ошибок
  def __init__   (self,log:Log,UI:appUI.Window,initLogStr:str):
    self.log,self.UI = log,UI
    self.queue       = [] # текущая очередь
    self.qStage      = [] # q=queue: ошибки после очереди, ждут записи
    self.qFinal      = [] # q=queue: храним ошибки для подсчёта в самом конце
    self.file        = G.files['errors']
    self.write(initLogStr,False)
  def  addCur    (self,errors:dict):  # errors={initLow:ErrorObj,...}
    def _addUI():
      vars   = {'count':str(len(err.pos)),
                'value':        err.initVal}
      txt    = strF.replaceVars(S.log['errQueue'],vars)
      err.UI = self.UI.buildUI('re:item',self.UI.wx['errQueue'],{'text':txt})
    self.queue = list(errors.values())
    for  err  in self.queue: _addUI()
    if errors: self.log.add('errorsFound',
                           {'type' :        self.queue[0].type,
                            'count':str(len(self.queue))})
  def suggClicked(self,OKclicked:bool,newValue:str,autoSkipped=False):
    def _log():
      if not autoSkipped:
        key =   'sugg'+('-','+')[err.fixed]
        self.log.add(key,{'type':err.type,'from':err.initVal,'to':err.newVal})
      if not err.fixed:
        self.write(S.log['errorLeft'].replace('$type$',err.type) + lblText)
    err     =   self.queue.pop(0)
    lblText = err.suggFinished(OKclicked,newValue)
    _log()
    self.qStage.append(err)
  def write      (self,str:str,justAdd=True):
    write_toFile (str ,self.file,justAdd)
    self.UI.buildUI('log',self.UI.wx['rl:errors'],{'text':str})
  def getCount   (self):
    final = 0
    for item in self.qFinal:
      if not item.fixed: final += len(item.pos)
    return final
class ErrorObj(): # объект одной ошибки, используется в хранилище Errors()
  def __init__(self,type:str,initValue:str,pos:dict,initFixed=False,newVal=None):
    # pos={'r':row,'c':col}
    self.type    =  type  # тип ошибки, один из G.AStypes
    self.initVal =  initValue
    self. newVal =   newVal
    self.fixed   =  initFixed
    self.pos     = [pos]  # список всех позиций в диапазоне проверки [{'r':,'c':},...]
    self.UI      =  None  # при создании очереди queue тут появится ссылка на label
  def addPos  (self,pos :dict): self.pos.append(pos)
  def suggFinished(self,fixed:bool,newVal:str):
    self.fixed,self.newVal = fixed,newVal
    txt = self.UI['text']
    self.UI.destroy()
    self.UI = None
    return txt

# защита от запуска модуля
if __name__ == '__main__':
  print  ("This is module, please don't execute.")
  SYSEXIT()
