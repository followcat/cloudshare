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
};

export const getAPI = {
  BOOKMARK_API: (id) => { return `${API.ACCOUNTS_API}/${id}/bookmark` },
}

export const URL = {
  getResumeURL: (id) => {
    return `/resume/${id}`; 
  },
};
