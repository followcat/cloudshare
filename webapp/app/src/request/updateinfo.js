'use strict';
import StorageUtil from '../utils/storage';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const updateInfo = (params, callback) => {
  return fetch(API.USER_API, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json))
};
