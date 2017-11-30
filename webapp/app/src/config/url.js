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

  getJobSearchURL: () => {
    return `/jobsearch`;
  },

  getProJobSearchURL: () => {
    return `/jobsearch/result?search_text=`;
  },

  getUploaderURL: () => {
    return `/uploader`;
  },

  getProUploaderURL: () => {
    return `/prouploader`;
  },
  
  getAddPositionURL: () => {
    return `/addposition`;
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
  getInvitedMessageURL: () => {
    return `/notice/invitedmessage`;
  },
  getInviterMessageURL: () => {
    return `/notice/invitermessage`;
  },
  getUnreadMessageURL: () => {
    return `/notice/unreadmessage`;
  },
  getProcessedMessageURL: () => {
    return `/notice/processedmessage`;
  },
  getReadMessageURL: () => {
    return `/notice/readmessage`;
  },
  getSentMessageURL: () => {
    return `/notice/sentmessage`;
  },
  getBecomeMember: () => {
    return `/becomemember`;
  },
  getManagement: () => {
    return `/management`;
  },
};
