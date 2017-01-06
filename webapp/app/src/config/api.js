'use strict';
const HOST = '';

export const API = {

  ACCOUNTS_API: `${HOST}/api/accounts`,

  ADDITIONALS_API: `${HOST}/api/additionnames`,

  CLASSIFY_API: `${HOST}/api/classify`,

  COMPANYLIST_API: `${HOST}/api/companylist`,

  COMPANY_API: `${HOST}/api/company`,

  ALL_COMPANY_API: `${HOST}/api/companyall`,

  ALL_COMPANY_BY_SEARCH_API: `${HOST}/api/searchcobytext`,

  UPDATE_COMPANY_INFO_API: `${HOST}/api/companyinfoupdate`,

  CUSTOMER_LIST_API: `${HOST}/api/customerlist`,

  CUSTOMER_API: `${HOST}/api/customer`,

  CREATE_JOBDESCRIPTION_API: `${HOST}/api/uploadjd`,

  FEATURE_API: `${HOST}/api/feature`,

  JOBDESCRIPTION_API: `${HOST}/api/jdlist`,

  PROJECTS_API: `${HOST}/api/projectnames`,

  SEARCH_BY_TEXT_API: `${HOST}/api/searchbytext`,

  SESSION_API: `${HOST}/api/session`,

  UPLOAD_RESUME_API: `${HOST}/api/uploadcv`,

  UPLOAD_RESUME_PREVIEW_API: `${HOST}/api/uploadcv/preview`,

  UPLOAD_ENGLISH_RESUME_API: `${HOST}/api/uploadengcv`,

  UPLOAD_EXCEL_API: `${HOST}/api/couploadexcel`,

  BOOKMARK_API: `bookmark`,  // {host}/api/accounts/{id}/bookmark

  UPDATE_JOBDESCRIPTION_API: `${HOST}/api/jd`,  // {host}/api/jd/{id}

  LSI_BY_JD_ID_API: `${HOST}/api/mining/lsibyjdid`,

  LSI_BY_CV_ID_API: `${HOST}/api/mining/lsibycvid`,

  LSI_BY_DOC_API: `${HOST}/api/mining/lsibydoc`,
};