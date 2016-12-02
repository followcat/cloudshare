'use strict';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import 'whatwg-fetch';

export const uploadPreview = (params, callback) => {
  return fetch(`${API.UPLOAD_RESUME_PREVIEW_API}`, {
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


export const confirmUpload = (params, callback) => {
  return fetch(`${API.UPLOAD_RESUME_API}`, {
    method: 'PUT',
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