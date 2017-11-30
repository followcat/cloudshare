'use strict';
import StorageUtil from 'utils/storage';
import Generator from 'utils/generator';
import { API } from 'config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const jdMatching = (params,callback) => {
  return fetch(API.MINING_JD_MATCING_API, {
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

export const proJdMatching = (params,callback) => {
  return fetch(`${API.MINING_JD_MATCING_API}?${params.numbers}&${params.page}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};