'use strict';
import { API } from 'config/api';
import StorageUtil from 'utils/storage';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const readMessage = (params, callback) => {
  return fetch(`${API.MESSAGE_API}/${params.msgid}`, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

/**
 * 获取message列表数据请求
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getListInvited = (callback) => {
  return fetch(API.LIST_INVITED_MESSAGES_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

export const getListInviter = (callback) => {
  return fetch(API.LIST_INVITER_MESSAGES_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

export const getListProcessed = (callback) => {
  return fetch(API.LIST_PROCESSED_MESSAGES_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

export const getListRead = (callback) => {
  return fetch(API.LIST_READ_MESSAGES_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

export const getListUnread = (callback) => {
  return fetch(API.LIST_UNREAD_MESSAGES_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

export const getListSent = (callback) => {
  return fetch(API.LIST_SENT_MESSAGES_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};

export const deleteMessage = (params, callback) => {
  return fetch(`${API.MESSAGE_API}/${params.msgid}`, {
    method: 'DELETE',
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

export const acceptInviteMessage = (params, callback) => {
  return fetch(`${API.ACCEPT_INVITE_MESSAGE_API}/${params.msgid}`, {
    method: 'POST',
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

export const messagesNotify = (callback) => {
  return fetch(API.MESSAGESNOTIFY_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
  })
  .then(response => response.json())
  .then(json => {
    callbackFunction(callback, json);
  });
};