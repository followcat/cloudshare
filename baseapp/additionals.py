import interface.predator
import services.curriculumvitae


PREDATOR_DB = interface.predator.PredatorInterface('additional/liepin')
PRE_SVC_CV = services.curriculumvitae.CurriculumVitae(PREDATOR_DB, 'liepin')

JINGYING_DB = interface.predator.PredatorInterface('additional/jingying')
JGYG_SVC_CV = services.curriculumvitae.CurriculumVitae(JINGYING_DB, 'jingying')

ZHILIAN_DB = interface.predator.PredatorInterface('additional/zhilian')
ZILN_SVC_CV = services.curriculumvitae.CurriculumVitae(ZHILIAN_DB, 'zhilian')

YINGCAI_DB = interface.predator.PredatorInterface('additional/yingcai')
YICA_SVC_CV = services.curriculumvitae.CurriculumVitae(YINGCAI_DB, 'yingcai')
