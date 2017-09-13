'use strict';
import StorageUtil from '../utils/storage';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const elevateAdmin = (params,callback) => {
  return fetch(API.MEMBER_ADMIN_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body:JSON.stringify(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const revokeAdmin = (params,callback) => {
  return fetch(API.MEMBER_ADMIN_API, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body:JSON.stringify(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};