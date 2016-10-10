'use strict';
import Storage from './storage';

const addBasemodel = (postData) => {
  let basemodel = Storage.get('_pj');
  return Object.assign(postData, { basemodel: basemodel });
};

const Generator = {
  getPostData: (postData) => {
    postData = addBasemodel(postData);
    return JSON.stringify(postData);
  },
};

module.exports = Generator;