'use strict';
import StorageUtil from '../utils/storage';
import { API } from './api';
import 'whatwg-fetch';

const callbackFunction = (callback, json) => {
  if (callback && typeof callback === 'function') {
    callback(json);
  }
}

/**
 * 用户登陆请求
 * @param  {object}   params   请求参数
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const signIn = (params, callback) => {
  console.log(params)
  return fetch(API.SESSION_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

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

/**
 * 获取project列表数据请求
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getProject = (callback) => {
  return fetch(API.PROJECTS_API, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};
