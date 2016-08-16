import interface.gitinterface
import services.curriculumvitae


DATA_DB_NAME = 'repo'
DATA_DB = interface.gitinterface.GitInterface(DATA_DB_NAME)
DEF_SVC_CV = services.curriculumvitae.CurriculumVitae(DATA_DB, 'cloudshare')
