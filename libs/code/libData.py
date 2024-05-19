from sys import exit as SYSEXIT

# столбцы; иначе не влезает на экран :/ будет храниться в виде {'city':{'title':X,'type':Y,...},...}
colKeys   =                      ['title',                                 'type',       'mandatory', 'maxUnique', 'maxWidth', 'textWrapping']
colValues = {'city'            : ['Регион и город'                       , 'city'            , True ,  99999     ,  0        ,  False        ],
             'cat'             : ['Категория'                            , 'cat'             , True ,  2         ,  0        ,  False        ],
             'vert'            : ['Вертикаль'                            , 'vert'            , True ,  1         ,  0        ,  False        ],
             'source'          : ['Источник'                             , 'source'          , True ,  1         ,  0        ,  False        ],
             'coreLT'          : ['Направление клиента'                  , 'coreLT'          , False,  1         ,  0        ,  False        ],
             'microCat'        : ['Микрокатегория'                       , 'microCat'        , False,  2         ,  0        ,  False        ],
             'clientStatus'    : ['Статус клиента'                       , 'clientStatus'    , False,  2         ,  0        ,  False        ],
             'clientSpends'    : ['Траты клиента в месяц'                , 'clientSpends'    , False,  99999     ,  0        ,  False        ],
             'manager'         : ['Ответственный менеджер в сделке'      , 'manager'         , False,  2         ,  0        ,  False        ],
             'leadName'        : ['Название лида'                        , 'leadName'        , True ,  1         ,  0        ,  False        ],
             'projName'        : ['Наименование проекта'                 , 'projName'        , True ,  1         ,  0        ,  False        ],
             'companyName'     : ['Название компании'                    , 'companyName'     , True ,  99999     ,  0        ,  False        ],
             'pFamily'         : ['Фамилия'                              , None              , False,  99999     ,  0        ,  False        ],
             'pName'           : ['Имя'                                  , 'nonEmpty'        , True ,  99999     ,  0        ,  False        ],
             'pOtch'           : ['Отчество'                             , None              , False,  99999     ,  0        ,  False        ],
             'jobTitle'        : ['Должность'                            , None              , False,  99999     ,  0        ,  False        ],
             'mainPhone'       : ['Основной телефон'                     , 'phone'           , True ,  99999     ,  0        ,  False        ],
             'secPhone'        : ['Другой телефон'                       , 'phone'           , False,  99999     ,  0        ,  False        ],
             'addPhone'        : ['Добавочный телефон'                   , 'numbers any'     , False,  99999     ,  0        ,  False        ],
             'mainMail'        : ['Рабочий e-mail'                       , 'mail'            , False,  99999     ,  0        ,  False        ],
             'secMail'         : ['Частный e-mail'                       , 'mail'            , False,  99999     ,  0        ,  False        ],
             'mainWebsite'     : ['Корпоративный сайт'                   , 'website'         , False,  99999     ,  0        ,  False        ],
             'secWebsite'      : ['Другой сайт'                          , 'website'         , False,  99999     ,  0        ,  False        ],
             'avitoID'         : ['Авито-аккаунт'                        , 'numbers < 10'    , False,  99999     ,  0        ,  False        ],
             'INN'             : ['ИНН'                                  , 'numbers any'     , False,  99999     ,  0        ,  False        ],
             'idTAM'           : ['ID TAM'                               , 'numbers any'     , False,  99999     ,  0        ,  False        ],
             'TAMsegment'      : ['TAM сегмент'                          , None              , False,  4         ,  0        ,  False        ],
             'comment'         : ['Комментарий'                          , None              , False,  99999     ,  0        ,  True         ],
             'eventDate'       : ['Дата проведения мероприятия'          , 'date'            , False,  1         ,  0        ,  False        ],
             'eventVisitStatus': ['Статус посещения мероприятия клиентом', 'eventVisitStatus', False,  3         ,  0        ,  False        ],
             'landingID'       : ['Обозначения лида на лендинге'         , None              , False,  1         ,  0        ,  False        ],
             'advID'           : ['Обозначение рекламной кампании'       , None              , False,  1         ,  0        ,  False        ],
             'leadOwner'       : ['Ответственный'                        , 'leadOwner'       , True ,  1         ,  0        ,  False        ],
             'leadAvail'       : ['Доступен для всех'                    , 'leadAvail'       , True ,  1         ,  0        ,  False        ]}

# защита от запуска модуля
if __name__ == '__main__':
    print  ("This is module, please don't execute.")
    SYSEXIT()
