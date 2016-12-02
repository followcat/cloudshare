'use strict';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import StorageUtil from '../utils/storage';

export const getClassify = (callback) => {
  return fetch(API.ADDITIONALS_API, {
    method: 'GET',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`
    }
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};
