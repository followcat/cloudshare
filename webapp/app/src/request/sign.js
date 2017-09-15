'use strict';
import StorageUtil from 'utils/storage';
import { API } from 'config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

/**
 * 用户登陆请求
 * @param  {object}   params   请求参数
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const signIn = (params, callback) => {
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
 * 用户登出请求
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const signOut = (callback) => {
  return fetch(API.SESSION_API, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`
    }
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  })
};
