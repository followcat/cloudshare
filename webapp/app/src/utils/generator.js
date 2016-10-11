'use strict';
import Storage from './storage';

const addBasemodel = (postData={}) => {
  let project = Storage.get('_pj');
  return Object.assign(postData, { project: project });
};

const Generator = {
  getPostData: (postData={}) => {
    postData = addBasemodel(postData);
    return JSON.stringify(postData);
  },
};

module.exports = Generator;