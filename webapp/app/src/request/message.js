'use strict';
import { API } from '../config/api';
import StorageUtil from '../utils/storage';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

/**
 * 获取message列表数据请求
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getListInvited = (callback) => {
  return fetch(API.LIST_INVITED_MESSAGES_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};