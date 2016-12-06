'use strict';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import StorageUtil from '../utils/storage';
import 'whatwg-fetch';

export const getEnglishResume = (callback) => {
  return fetch(API.UPLOAD_ENGLISH_RESUME, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`
    }
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};