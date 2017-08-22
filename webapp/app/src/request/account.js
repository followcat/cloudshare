'use strict';
import StorageUtil from '../utils/storage';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const getAccounts = (callback) => {
  return fetch(API.ACCOUNTS_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`
    }
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const checkAccount = (params,callback) => {
  return fetch(`${API.ACCOUNT_API}/${params.name}`, {
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

export const getAccount = (params,callback) => {
  return fetch(API.USER_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    }
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const createAccount = (params, callback) => {
  return fetch(`${API.ACCOUNT_API}/${params.name}`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      // 'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const deleteAccount = (userId, callback) => {
  return fetch(`${API.ACCOUNTS_API}/${userId}`, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
    },
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
}