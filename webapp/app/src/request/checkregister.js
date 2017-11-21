'use strict';
import StorageUtil from 'utils/storage';
import { API } from 'config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const checkEmail = (params,callback) => {
  return fetch(`${API.EXISTS_EMAIL_API}/${params.email}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const checkPhone = (params,callback) => {
  return fetch(`${API.EXISTS_PHONE_API}/${params.phone}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};