'use strict';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

/**
 * 获取feature数据请求
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getFeature = (callback) => {
  return fetch(API.FEATURE_API, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};
