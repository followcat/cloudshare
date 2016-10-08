#encoding: utf-8
import yaml


with open('sources/industry_needed_medical.yaml') as f:
    needed_medical = yaml.load(f.read())

with open('sources/industry_needed_uav.yaml') as f:
    needed_uav = yaml.load(f.read())

with open('sources/industry_sources.yaml') as f:
    sources = yaml.load(f.read())

industryID = {
        u'培训':'0',
        u'服装/纺织/皮革':'1',
        u'汽车':'2',
        #u'销售管理':'3',
        u'通信技术开发及应用':'4',
        #u'采购':'5',
        u'建筑装潢/市政建设':'6',
        u'农/林/牧/渔':'7',
        u'影视/媒体':'8',
        u'写作/出版/印刷':'9',
        u'生物/制药/医疗器械':'10',
        u'广告':'11',
        #u'教师':'12',
        #u'人力资源':'13',
        u'律师/法务/合规':'14',
        u'市场/营销':'15',
        u'物业管理':'16',
        u'金融/证券/期货/投资':'17',
        u'百货/连锁/零售服务':'18',
        #u'高级管理':'19',
        #u'物流/仓储':'20',
        u'化工':'21',
        u'酒店/旅游':'22',
        u'保险':'23',
        u'其他':'24',
        u'房地产':'25',
        u'公务员':'26',
        #u'储备干部/培训生/实习生':'27',
        #u'翻译':'28',
        #u'行政/后勤':'29',
        u'电子/电器/半导体/仪器仪表':'30',
        #u'IT/管理':'31',
        u'计算机硬件':'32',
        u'餐饮/娱乐':'33',
        u'工程/机械/能源':'34',
        u'科研人员':'35',
        #u'兼职':'36',
        #u'艺术/设计':'37',
        u'交通运输服务':'38',
        u'质量管理/安全防护':'39',
        u'贸易':'40',
        #u'技工':'41',
        u'计算机软件':'42',
        u'保安/家政/其他服务':'43',
        u'环保':'44',
        u'咨询/顾问':'45',
        u'生产/营运':'46',
        u'互联网/电子商务/网游':'47',
        #u'客服及技术支持':'48',
        #u'销售行政及商务':'49',
        u'IT/品管、技术支持及其它':'50',
        u'公关/媒介':'51',
        u'医院/医疗/护理':'52',
        u'财务/审计/税务':'53',
        #u'销售人员':'54',
        #u'在校学生':'55',
        u'美容/健身/体育':'56',
        u'银行':'57',
        u'航空/航天':'58'
        }
