'use strict';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const getFastMatching = (api, params, callback) => {
  return fetch(api, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};
