'use strict';
import StorageUtil from '../utils/storage';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const getListCustomer = (callback) => {
  return fetch(API.LIST_CUSTOMER_ACCOUNTS_API, {
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

export const deleteCustomer = (params,callback) => {
  return fetch(`${API.ACCEPT_INVITE_MESSAGE_API}/${params.customerName}`, {
    method: 'DELETE',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const sendInviteMessage = (params,callback) => {
  return fetch(`${API.SEND_INVITE_MESSAGE_API}/${params.customerName}`, {
    method: 'POST',
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

export const isCustomer = (callback) => {
  return fetch(API.IS_CUSTOMER_API, {
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

export const isCustomerAdmin = (callback) => {
  return fetch(API.IS_CUSTOMER_ADMIN_API, {
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