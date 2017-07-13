'use strict';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import Generator from '../utils/generator';
import StorageUtil from '../utils/storage';

export const getClassify = (callback) => {
  return fetch(API.CLASSIFY_API, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData()
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const getLSIAllSIMS = (callback) => {
  return fetch(API.LSIALLSIMS_API, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData()
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const getIndustry = (callback) => {
  return fetch(API.INDUSTRY_API, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData()
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};
