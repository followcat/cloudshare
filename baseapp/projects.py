#encoding: utf-8
import os

import services.projectcv
from baseapp.datadbs import *


PRJ_PATH = 'projects'
if not os.path.exists(PRJ_PATH):
    os.makedirs(PRJ_PATH)

MED_needed = [
                u'航空-航天',
                u'计算机软件',
                u'计算机硬件',
                u'生物-制药-医疗器械',
                u'通信技术开发及应用',
                u'电子-电器-半导体-仪器仪表',
                u'科研人员',
                u'汽车',
                u'建筑装潢-市政建设',
                u'律师-法务-合规',
                u'市场-营销',
                u'化工',
                u'房地产',
                u'工程-机械-能源',
                u'交通运输服务',
                u'质量管理-安全防护',
                u'环保',
                u'咨询-顾问',
                u'生产-营运',
                u'互联网-电子商务-网游',
                u'IT-品管、技术支持及其它',
                u'医院-医疗-护理',
                u'财务-审计-税务',
                ]


UAV_needed = [
                u'通信技术开发及应用',
                u'计算机硬件',
                u'计算机软件',
                u'航空-航天',
                u'电子-电器-半导体-仪器仪表',
                u'科研人员'
                ]

MED_DB = interface.gitinterface.GitInterface(os.path.join(PRJ_PATH, 'medical'))
SVC_PRJ_MED = services.projectcv.ProjectCV(MED_DB, SVC_CV_REPO, 'medical')
SVC_PRJ_MED.setup(MED_needed)

UAV_DB = interface.gitinterface.GitInterface(os.path.join(PRJ_PATH, 'UAV'))
SVC_PRJ_UAV = services.projectcv.ProjectCV(UAV_DB, SVC_CV_REPO, 'UAV')
SVC_PRJ_UAV.setup(UAV_needed)
