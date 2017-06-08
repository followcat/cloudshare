'use strict';
import StorageUtil from '../utils/storage';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

const BOOKMARK_API = `${API.ACCOUNTS_API}/${StorageUtil.get('user')}/${API.BOOKMARK_API}`;

/**
 * 获取书签列表
 * @param  {function} callback 回调方法
 * @return {function} fetch    异步请求
 */
export const getBookmark = (callback) => {
  return fetch(BOOKMARK_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
    },
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/**
 * 添加简历到书签
 * @param {object} params 简历Id
 * @param {*} callback    回调方法
 */
export const addBookmark = (params, callback) => {
  return fetch(BOOKMARK_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(params),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/**
 * 删除书签
 * @param  {object} params 异步请求的参数对象
 * @param  {function} callback 回调方法
 * @return {function} fetch    异步请求
 */
export const deleteBookmark = (params, callback) => {
  return fetch(BOOKMARK_API, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};
