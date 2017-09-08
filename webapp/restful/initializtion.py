import flask.ext.restful

from webapp.restful.people import *
from webapp.restful.mining import *
from webapp.restful.reload import *
from webapp.restful.upload import *
from webapp.restful.account import *
from webapp.restful.company import *
from webapp.restful.message import *
from webapp.restful.customer import *
from webapp.restful.captchaverify import *
from webapp.restful.jobdescription import *
from webapp.restful.curriculumvitae import *
from webapp.restful.feature import *
from webapp.restful.session import *
from webapp.restful.bookmark import *
from webapp.restful.databases import *

def initialize(app):
    api = flask.ext.restful.Api(app)
    api.add_resource(SyncReloadAPI, '/api/syncreload', endpoint = 'syncreload')
    api.add_resource(SessionAPI, '/api/session')
    api.add_resource(PasswordAPI, '/api/password')
    api.add_resource(UserAPI, '/api/user', endpoint = 'user')
    api.add_resource(AccountAPI, '/api/account/<string:name>', endpoint = 'account')
    api.add_resource(AccountListAPI, '/api/accounts', endpoint = 'accounts')
    api.add_resource(AccountHistoryAPI, '/api/accounthistory', endpoint = 'accounthistory')

    api.add_resource(BookmarkAPI, '/api/accounts/<string:name>/bookmark')

    api.add_resource(CompanyAPI, '/api/company', endpoint = 'company')
    api.add_resource(CompanyAllAPI, '/api/companyall', endpoint = 'companyall')
    api.add_resource(AddedCompanyListAPI, '/api/addedcompanylist', endpoint = 'adddedcompanylist')
    api.add_resource(CompanyUploadExcelAPI, '/api/couploadexcel',
                     endpoint = 'couploadexcel')
    api.add_resource(CompanyConfirmExcelAPI, '/api/coconfirmexcel',
                     endpoint = 'coconfirmexcel')
    api.add_resource(CompanyCustomerListAPI, '/api/companycustomerlist',
                     endpoint = 'companycustomerlist')
    api.add_resource(SearchCObyTextAPI, '/api/searchcobytext', endpoint = 'searchcobytext')
    api.add_resource(SearchCObyKeyAPI, '/api/searchcobykey', endpoint = 'searchcobykey')
    api.add_resource(CompanyCustomerAPI, '/api/companycustomer', endpoint = 'companycustomer')
    api.add_resource(CompanyInfoUpdateAPI, '/api/companyinfoupdate',
                     endpoint = 'companyinfoupdate')

    api.add_resource(JobDescriptionUploadAPI, '/api/uploadjd',
                     endpoint = 'jobdescriptionupload')
    api.add_resource(JobDescriptionAPI, '/api/jd',
                     endpoint = 'jobdescription')
    api.add_resource(JobDescriptionListAPI, '/api/jdlist',
                     endpoint = 'jobdescriptionlist')

    api.add_resource(CurrivulumvitaeAPI, '/api/resume',
                     endpoint = 'curriculumvitae')
    api.add_resource(UpdateCurrivulumvitaeInformation, '/api/cv/updateinfo',
                     endpoint = 'updatecurrivulumvitaeinformation')

    api.add_resource(UploadCVAPI, '/api/uploadcv', endpoint = 'uploadcv')
    api.add_resource(UploadEnglishCVAPI, '/api/uploadengcv', endpoint = 'uploadengcv')
    api.add_resource(UploadCVPreviewAPI, '/api/uploadcv/preview')

    api.add_resource(SearchCVbyTextAPI, '/api/searchbytext', endpoint = 'searchbytext')

    api.add_resource(RegionAPI, '/api/mining/region', endpoint = 'region')
    api.add_resource(CapacityAPI, '/api/mining/capacity', endpoint = 'capacity')
    api.add_resource(PositionAPI, '/api/mining/position', endpoint = 'position')

    api.add_resource(AbilityAPI, '/api/mining/ability', endpoint = 'ability')
    api.add_resource(ExperienceAPI, '/api/mining/experience', endpoint = 'experience')

    api.add_resource(LSIbydocAPI, '/api/mining/lsibydoc', endpoint = 'lsibydoc')

    api.add_resource(LSIbyJDidAPI, '/api/mining/lsibyjdid', endpoint = 'lsibyjdid')
    api.add_resource(LSIbyAllJDAPI, '/api/mining/lsibyalljd', endpoint = 'lsibyalljd')
    api.add_resource(LSIbyCVidAPI, '/api/mining/lsibycvid', endpoint = 'lsibycvid')

    api.add_resource(SimilarAPI, '/api/mining/similar', endpoint = 'similar')

    api.add_resource(ValuableAPI, '/api/mining/valuable')

    api.add_resource(ValuablebyJDidAPI, '/api/mining/valuablebyjdid',
                                        endpoint = 'valuablebyjdid')
    api.add_resource(ValuablebydocAPI, '/api/mining/valuablebydoc',
                                        endpoint = 'valuablebydoc')

    api.add_resource(FeatureAPI, '/api/feature', endpoint = 'feature')


    api.add_resource(PeopleAPI, '/api/people', endpoint = 'people')
    api.add_resource(PeopleByCVAPI, '/api/peoplebycv', endpoint = 'peoplebycv')

    api.add_resource(ProjectNamesAPI, '/api/projectnames', endpoint = 'projectnames')
    api.add_resource(AdditionNamesAPI, '/api/additionnames', endpoint = 'additionnames')
    api.add_resource(DBNumbersAPI, '/api/dbnumbers', endpoint = 'dbnumbers')
    api.add_resource(ClassifyAPI, '/api/classify', endpoint = 'classify')
    api.add_resource(AllSIMSAPI, '/api/lsiallsims', endpoint = 'lsiallsims')
    api.add_resource(IndustryAPI, '/api/industry', endpoint = 'industry')

    api.add_resource(MessageAPI, '/api/message/<string:msgid>',
                     endpoint = 'message')
    api.add_resource(MessagesNotifyAPI, '/api/messagenotify',
                     endpoint = 'messagenotify')
    api.add_resource(SendMessageAPI, '/api/sendmessage/<string:desname>',
                     endpoint = 'sendmessage')
    api.add_resource(InvitedMessageAPI, '/api/invitedmessage/<string:msgid>',
                     endpoint = 'invitedmessage')
    api.add_resource(SendInviteMessageAPI, '/api/sendinvitemessage/<string:desname>',
                     endpoint = 'sendinvitemessage')
    api.add_resource(ListReadMessagesAPI, '/api/listreadmessages', endpoint = 'listreadmessages')
    api.add_resource(ListUnreadMessagesAPI, '/api/listunreadmessages', endpoint = 'listunreadmessages')
    api.add_resource(ListInvitedMessagesAPI, '/api/listinvitedmessages', endpoint = 'listinvitedmessages')

    api.add_resource(IsCustomerAPI, '/api/iscustomer', endpoint = 'iscustomer')
    api.add_resource(IsCustomerAdminAPI, '/api/iscustomeradmin', endpoint = 'iscustomeradmin')
    api.add_resource(CustomerAPI, '/api/customer', endpoint = 'customer')
    api.add_resource(CustomerAdminAPI, '/api/customeradmin', endpoint = 'customeradmin')
    api.add_resource(ListCustomerAccountsAPI, '/api/listcustomeraccounts',
                     endpoint = 'listcustomeraccounts')
    api.add_resource(CustomerAccountAPI, '/api/customeraccount/<string:userid>',
                     endpoint = 'customeraccount')
    api.add_resource(CustomerProjectAPI, '/api/customerproject/<string:projectname>',
                     endpoint = 'customerproject')

    api.add_resource(CaptchaAPI, '/api/captcha', endpoint = 'captcha')
