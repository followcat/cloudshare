'use strict';

const url = {
  ZHILIAN: `http://h.highpin.cn`,
  JINGYING: `http://www.51jingying.com`,
  LIEPIN: `https://h.liepin.com`,
  YINGCAI: '',
};


const getSourceURL = (website, cvURL) => {
  let sourceURL = '';
  switch (true) {
    case website.indexOf('智联卓聘') > -1:
      sourceURL = url.ZHILIAN + cvURL;
      break;
    case website.indexOf('无忧精英') > -1:
      sourceURL = url.JINGYING + cvURL;
      break;
    case website.indexOf('猎聘') > -1:
      sourceURL = url.LIEPIN + cvURL;
      break;
    case website.indexOf('中华英才') > -1:
      sourceURL = url.YINGCAI + cvURL;
      break;
    default:
      break;
  }
  return sourceURL;
};

export { getSourceURL };
