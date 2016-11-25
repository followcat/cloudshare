'use strict';
const HOST = '';

export const API = {
  FEATURE_API: `${HOST}/api/feature`,
  SESSION_API: `${HOST}/api/session`,
  PROJECTS_API: `${HOST}/api/projectnames`,
  ACCOUNTS_API: `${HOST}/api/accounts`,
  SEARCH_BY_TEXT_API: `${HOST}/api/searchbytext`,
  CLASSIFY_API: `${HOST}/api/classify`,
  ADDITIONALS_API: `${HOST}/api/additionnames`,
  JOBDESCRIPTION_API: `${HOST}/api/jdlist`,
  CREATE_JOBDESCRIPTION_API: `${HOST}/api/uploadjd`,
  COMPANYLIST_API: `${HOST}/api/companylist`,
  COMPANY_API: `${HOST}/api/company`,
};

export const getAPI = {
  BOOKMARK_API: (id) => { return `${API.ACCOUNTS_API}/${id}/bookmark`; },
  UPDATE_JOBDESCRIPTION_API: (id) => { return `${HOST}/api/jd/${id}`; },
}

export const URL = {
  getSearchURL: () => {
    return `/search`;
  },

  getResumeURL: (id) => {
    return `/resume/${id}`; 
  },

  getUserInfoURL: () => {
    return `/userinfo`;
  },

  getUploaderURL: () => {
    return `/uploader`;
  },

  getListJDURL: () => {
    return `/listjd`;
  },

  getFastMatching: (id) => {
    return `/fastmatching?jd_id=${id}`;
  }
};
