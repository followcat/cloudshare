'use strict';
import StorageUtil from 'utils/storage';
import Generator from 'utils/generator';
import { API } from 'API';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const getDatabaseInfo = (callback) => {
  return fetch(API.DATABASE_INFO_API, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData()
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

export const getResultData = (params, callback) => {
  return fetch(API.SEARCH_BY_TEXT_API, {
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
  .then(json => {
    callbackFunction(callback, json);
  });
};
