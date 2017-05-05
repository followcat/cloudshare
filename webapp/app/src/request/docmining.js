'use strict';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

import { API } from 'API';

export const getDocMining = (api, params, callback) => {
  return fetch(api, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const getDocMiningCV = (params, callback) => {
  return fetch(API.MINING_CV_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};
