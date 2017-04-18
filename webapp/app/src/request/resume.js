'use strict';
import { API } from 'API';
import { callbackFunction } from './callback';
import StorageUtil from 'utils/storage';
import Generator from 'utils/generator';
import 'whatwg-fetch';

export const getEnglishResume = (callback) => {
  return fetch(API.UPLOAD_ENGLISH_RESUME_API, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`
    }
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 获取简历信息
export const getResumeInfo = (params, callback) => {
  return fetch(API.RESUME_INFO_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 获取相似候选人列表
export const getSimilar = (params, callback) => {
  return fetch(API.SIMILAR_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 获取所有简历id列表
export const getResumeList = (params, callback) => {
  return fetch(API.RESUME_LIST_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 获取跟进, 评论, 标签信息
export const getAdditionalInfo = (params, callback) => {
  return fetch(API.ADDITIONAL_INFO_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 更新简历信息
export const updateResumeInfo = (params, callback) => {
  return fetch(API.UPDATE_RESUME_INFO_API, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 更新标签, 跟进, 评论信息
export const updateAdditionalInfo = (params, callback) => {
  return fetch(API.ADDITIONAL_INFO_API, {
    method: 'PUT',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};