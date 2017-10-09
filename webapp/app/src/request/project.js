'use strict';
import { API } from 'config/api';
import StorageUtil from 'utils/storage';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

/**
 * 获取project列表数据请求
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getProject = (callback) => {
  return fetch(API.PROJECTS_API, {
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
/**
 * add project
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const addProject = (params,callback) => {
  return fetch(`${API.MEMBER_PROJECT_API}/${params.projectname}`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
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
