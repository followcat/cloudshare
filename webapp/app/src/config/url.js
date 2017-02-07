'use strict';

export const URL = {

  getFastMatching: (id, append_commentary) => {
    return `/fastmatching?jd_id=${id}&init_append_commentary=${append_commentary}`;
  },

  getFastMatchingByCV: (id) => {
    return `/fastmatching?cv_id=${id}`
  },

  getFastMatchingByDoc: () => {
    return `/fastmatching`
  },

  getListJDURL: () => {
    return `/pm`;
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

  getDownloadURL: (id, fileName) => {
    return `/download/${id}`;
  },

  getProjectManagement: () => {
    return `/pm`;
  },

};
