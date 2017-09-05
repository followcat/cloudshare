'use strict';

export const URL = {

  getFastMatching: (id, append_commentary) => {
    return `/fastmatching?jd_id=${id}&init_append_commentary=${append_commentary}`;
  },

  getFastMatchingByCV: (id) => {
    return `/fastmatching?cv_id=${id}`;
  },

  getFastMatchingByDoc: () => {
    return `/fastmatching`;
  },

  getDocMining: () => {
    return `/docmining`;
  },

  getCVDocMining: () => {
    return `/cvdocmining`;
  },

  getCVsDocMining: () => {
    return `/cvsdocmining`;
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
    return `/userinfo/history`;
  },

  getDownloadURL: (id, fileName) => {
    return `/download/${id}`;
  },

  getProjectManagement: () => {
    return `/pm/jobdescription`;
  },

  getBestExcellent: () => {
    return `/excellent`;
  },
  getProjectList: () => {
    return `/pm/projectlist`;
  },
  getNotcieURL: () => {
    return `/notice`;
  },
  getInviteMessageURL: () => {
    return `/notice/invitemessage`;
  },

};
