'use strict';

export const URL = {

  getFastMatching: (id) => {
    return `/fastmatching?jd_id=${id}`;
  },

  getFastMatchingByCV: (id) => {
    return `/fastmatching?cv_id=${id}`
  },

  getListJDURL: () => {
    return `/listjd`;
  },

  getPreview: () => {
    return `/preview`;
  },

  getResumeURL: (id) => {
    return `/resume/${id}`; 
  },

  getSearchURL: () => {
    return `/search`;
  },

  getUploaderURL: () => {
    return `/uploader`;
  },

  getUserInfoURL: () => {
    return `/userinfo`;
  },

};
