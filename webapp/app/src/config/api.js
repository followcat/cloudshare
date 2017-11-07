'use strict';
const HOST = '';

export const API = {
  EXISTS_EMAIL_API : `${HOST}/api/existsemail`,

  EXISTS_PHONE_API :`${HOST}/api/existsphone`,

  SMS_API :`${HOST}/api/sms`,

  CAPTCHA_API :`${HOST}/api/captcha`,

  MEMBER_ADMIN_API:`${HOST}/api/memberadmin`,

  MEMBER_API:`${HOST}/api/member`,

  IS_MEMBER_ADMIN_API:`${HOST}/api/ismemberadmin`,

  IS_MEMBER_API:`${HOST}/api/ismember`,

  MESSAGESNOTIFY_API:`${HOST}/api/messagenotify`,

  MESSAGE_API:`${HOST}/api/message`,

  ACCEPT_INVITE_MESSAGE_API:`${HOST}/api/invitedmessage`,

  LIST_UNREAD_MESSAGES_API:`${HOST}/api/listunreadmessages`,

  LIST_READ_MESSAGES_API:`${HOST}/api/listreadmessages`,

  LIST_SENT_MESSAGES_API:`${HOST}/api/listsentmessages`,

  LIST_INVITED_MESSAGES_API:`${HOST}/api/listinvitedmessages`,

  LIST_INVITER_MESSAGES_API:`${HOST}/api/listinvitermessages`,

  LIST_PROCESSED_MESSAGES_API:`${HOST}/api/listprocessedmessages`,

  SEND_INVITE_MESSAGE_API:`${HOST}/api/sendinvitemessage`,

  MEMBER_ACCOUNT_API:`${HOST}/api/memberaccount`,

  LIST_MEMBER_ACCOUNTS_API:`${HOST}/api/listmemberaccounts`,

  MEMBER_PROJECT_API:`${HOST}/api/memberproject`,

  USER_API:`${HOST}/api/user`,

  PASSWORD_API: `${HOST}/api/password`,

  ACCOUNT_API: `${HOST}/api/account`,

  ACCOUNTS_API: `${HOST}/api/accounts`,

  ADDITIONALS_API: `${HOST}/api/additionnames`,

  CLASSIFY_API: `${HOST}/api/classify`,

  LSIALLSIMS_API: `${HOST}/api/lsiallsims`,

  INDUSTRY_API: `${HOST}/api/industry`,

  COMPANYLIST_API: `${HOST}/api/companylist`,

  COMPANY_API: `${HOST}/api/company`,

  ADDED_COMPANY_LIST_API: `${HOST}/api/addedcompanylist`,

  ALL_COMPANY_API: `${HOST}/api/companyall`,

  COMPANY_BY_SEARCH_TEXT_API: `${HOST}/api/searchcobytext`,
  
  COMPANY_BY_SEARCH_KEY_API: `${HOST}/api/searchcobykey`,

  UPDATE_COMPANY_INFO_API: `${HOST}/api/companyinfoupdate`,

  COMPANY_CUSTOMER_LIST_API: `${HOST}/api/companycustomerlist`,

  COMPANY_CUSTOMER_API: `${HOST}/api/companycustomer`,

  CREATE_JOBDESCRIPTION_API: `${HOST}/api/uploadjd`,

  FEATURE_API: `${HOST}/api/feature`,

  JOBDESCRIPTION_LIST_API: `${HOST}/api/jdlist`,

  JOBDESCRIPTION_API: `${HOST}/api/jd`,

  PROJECTS_API: `${HOST}/api/projectnames`,

  SEARCH_BY_TEXT_API: `${HOST}/api/searchbytext`,

  SESSION_API: `${HOST}/api/session`,

  UPLOAD_RESUME_API: `${HOST}/api/uploadcv`,

  UPLOAD_RESUME_PREVIEW_API: `${HOST}/api/uploadcv/preview`,

  UPLOAD_ENGLISH_RESUME_API: `${HOST}/api/uploadengcv`,

  UPLOAD_EXCEL_API: `${HOST}/api/couploadexcel`,

  CONFIRM_UPLOAD_EXCEL_API: `${HOST}/api/coconfirmexcel`,

  RESUME_INFO_API: `${HOST}/api/resume`,

  SIMILAR_API: `${HOST}/api/mining/similar`,

  RESUME_LIST_API: `${HOST}/api/peoplebycv`,

  ADDITIONAL_INFO_API: `${HOST}/api/people`,

  UPDATE_RESUME_INFO_API: `${HOST}/api/cv/updateinfo`,

  BOOKMARK_API: `bookmark`,  // {host}/api/accounts/{id}/bookmark

  //UPDATE_JOBDESCRIPTION_API: `${HOST}/api/jd`,  // {host}/api/jd/{id}

  LSI_BY_JD_ID_API: `${HOST}/api/mining/lsibyjdid`,

  LSI_BY_ALL_JD_API: `${HOST}/api/mining/lsibyalljd`,

  LSI_BY_CV_ID_API: `${HOST}/api/mining/lsibycvid`,

  LSI_BY_DOC_API: `${HOST}/api/mining/lsibydoc`,

  ANALYSIS_BY_DOC_API: `${HOST}/api/mining/analysisdoc`,

  MINING_CV_VALUABLE_API: `${HOST}/api/mining/cvvaluable`,

  DATABASE_INFO_API: `${HOST}/api/dbnumbers`,

  MINING_ABILITY_API: `${HOST}/api/mining/ability`,

  MINING_EXPERIENCE_API: `${HOST}/api/mining/experience`,

  MINING_POSITION_API: `${HOST}/api/mining/position`,

  MINING_VALUABLE_API: `${HOST}/api/mining/valuable`,

  MINING_CV_API: `${HOST}/api/mining/cv`,

  MINING_JD_MATCING_API: `${HOST}/api/mining/jdmatch`,
};

