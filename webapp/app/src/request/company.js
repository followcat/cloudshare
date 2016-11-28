'use strict';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import { API, getAPI } from './api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

/**
 * 获取公司列表
 * @param  {fucntion} callback [description]
 * @return {fucntion}            [description]
 */
export const getCompanys = (callback) => {
  return fetch(API.COMPANYLIST_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData(),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/**
 * 创建新的公司
 * @param  {object}   params   请求参数
 * @param  {function} callback 回调
 * @return {function} fetch    异步请求方法
 */
export const createCompany = (params, callback) => {
  return fetch(API.COMPANY_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData(params),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};
