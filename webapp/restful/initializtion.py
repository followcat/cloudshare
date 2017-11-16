import flask.ext.restful

from webapp.restful.match import *
from webapp.restful.people import *
from webapp.restful.mining import *
from webapp.restful.reload import *
from webapp.restful.upload import *
from webapp.restful.account import *
from webapp.restful.company import *
from webapp.restful.message import *
from webapp.restful.member import *
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
    api.add_resource(UserPeopleIDAPI, '/api/userpeopleid', endpoint = 'userpeopleid')
    api.add_resource(ExistsEmailAPI, '/api/existsemail/<string:email>', endpoint = 'existsemail')
    api.add_resource(ExistsPhoneAPI, '/api/existsphone/<string:phone>', endpoint = 'existsphone')
    api.add_resource(AccountAPI, '/api/account/<string:name>', endpoint = 'account')
    api.add_resource(AccountListAPI, '/api/accounts', endpoint = 'accounts')
    api.add_resource(AccountHistoryAPI, '/api/accounthistory', endpoint = 'accounthistory')

    api.add_resource(BookmarkAPI, '/api/accounts/<string:name>/bookmark')

    api.add_resource(CompanyAPI, '/api/company/<string:id>', endpoint = 'company')
    api.add_resource(CompanyAllAPI, '/api/companyall', endpoint = 'companyall')
    api.add_resource(AddedCompanyListAPI, '/api/addedcompanylist', endpoint = 'adddedcompanylist')
    api.add_resource(CompanyUploadExcelAPI, '/api/couploadexcel',
                     endpoint = 'couploadexcel')
    api.add_resource(CompanyConfirmExcelAPI, '/api/coconfirmexcel',
                     endpoint = 'coconfirmexcel')
    api.add_resource(CompanyCustomerListAPI, '/api/companycustomerlist',
                     endpoint = 'companycustomerlist')
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

    api.add_resource(UploadOriginsAPI, '/api/uploadorigins', endpoint = 'uploadorigins')
    api.add_resource(UserUploadCVAPI, '/api/userupcv', endpoint = 'userupcv')
    api.add_resource(MemberUploadCVAPI, '/api/memberupcv', endpoint = 'memberupcv')
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

    api.add_resource(JDmathAPI, '/api/mining/jdmatch', endpoint = 'jdmatch')
    api.add_resource(COmathAPI, '/api/mining/comatch', endpoint = 'comatch')
    api.add_resource(POSmathAPI, '/api/mining/posmatch', endpoint = 'posmatch')
    api.add_resource(PRJmathAPI, '/api/mining/prjmatch', endpoint = 'prjmatch')
    api.add_resource(CompanyProjectAPI, '/api/mining/coprjsearch', endpoint = 'coprjsearch')

    api.add_resource(FeatureAPI, '/api/feature', endpoint = 'feature')

    api.add_resource(PeopleAPI, '/api/people', endpoint = 'people')
    api.add_resource(PeopleByCVAPI, '/api/peoplebycv', endpoint = 'peoplebycv')

    api.add_resource(ProjectNamesAPI, '/api/projectnames', endpoint = 'projectnames')
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
    api.add_resource(ListSentMessagesAPI, '/api/listsentmessages', endpoint = 'listsentmessages')
    api.add_resource(ListUnreadMessagesAPI, '/api/listunreadmessages', endpoint = 'listunreadmessages')
    api.add_resource(ListInvitedMessagesAPI, '/api/listinvitedmessages', endpoint = 'listinvitedmessages')
    api.add_resource(ListInviterMessagesAPI, '/api/listinvitermessages', endpoint = 'listinvitermessages')
    api.add_resource(ListProcessedMessagesAPI, '/api/listprocessedmessages',
                     endpoint = 'listprocessedmessages')

    api.add_resource(IsMemberAPI, '/api/ismember', endpoint = 'ismember')
    api.add_resource(IsMemberAdminAPI, '/api/ismemberadmin', endpoint = 'ismemberadmin')
    api.add_resource(MemberAPI, '/api/member', endpoint = 'member')
    api.add_resource(MemberAdminAPI, '/api/memberadmin', endpoint = 'memberadmin')
    api.add_resource(ListMemberAccountsAPI, '/api/listmemberaccounts',
                     endpoint = 'listmemberaccounts')
    api.add_resource(MemberAccountAPI, '/api/memberaccount/<string:userid>',
                     endpoint = 'memberaccount')
    api.add_resource(MemberProjectAPI, '/api/memberproject/<string:projectname>',
                     endpoint = 'memberproject')

    api.add_resource(CaptchaAPI, '/api/captcha', endpoint = 'captcha')
    api.add_resource(SMSAPI, '/api/sms/<string:code>', endpoint = 'sms')
