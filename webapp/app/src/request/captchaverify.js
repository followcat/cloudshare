'use strict';
import StorageUtil from 'utils/storage';
import { API } from 'config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const getCaptcha = (callback) => {
  return fetch(API.CAPTCHA_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
    	'Cache-Control': 'no-cache'
    }
  })
  .then(response => response.blob())
  .then(blob => callbackFunction(callback, blob));
};

export const getSmscode = (params,callback) => {
  return fetch(`${API.SMS_API}/${params.captcha}`, {
    method: 'POST',
    credentials: 'include',
    headers: {
            'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};