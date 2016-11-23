'use strict';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import { API, getAPI } from './api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const getJobDescriptions = (callback) => {
  return fetch(API.JOBDESCRIPTION_API, {
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

export const createJobDescription = (params, callback) => {
  return fetch(API.CREATE_JOBDESCRIPTION_API, {
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

const getBodyData = (params) => {
  let obj = {};
  for (let key in params) {
    if (key !== 'id') {
      obj[key] = params[key];
    }
  }
  return obj;
};

export const updateJobDescription = (params, callback) => {
  return fetch(getAPI.UPDATE_JOBDESCRIPTION_API(params.id), {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData(getBodyData(params))
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};
