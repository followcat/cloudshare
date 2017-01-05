'use strict';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import { API } from '../config/api';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

/**
 * 获取客户公司列表
 * @param  {fucntion} callback [description]
 * @return {fucntion}            [description]
 */
export const getCompanys = (callback) => {
  return fetch(API.COMPANYLIST_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData(),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/**
 * 创建新的公司
 * @param  {object}   params   请求参数
 * @param  {function} callback 回调
 * @return {function} fetch    异步请求方法
 */
export const createCompany = (params, callback) => {
  return fetch(API.COMPANY_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData(params),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/* 
 * 获取所有公司列表
 * @param  {object}   params   请求参数: 页码, 每页条数
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getAllCompany = (params, callback) => {
  return fetch(API.ALL_COMPANY_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData(params),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/*
 * 获取公司列表搜索结果
 * @param  {object}   params   请求参数: 页码, 每页条数, 搜索关键字
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getAllCompanyBySearch = (params, callback) => {
  return fetch(API.ALL_COMPANY_BY_SEARCH_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData(params),
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/*
 * 更新公司信息
 * @param  {string}   method   请求方法: PUT(更新), DELETE(删除)
 * @param  {object}   params   请求参数
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const updateCompanyInfo = (method, params, callback) => {
  return fetch(API.UPDATE_COMPANY_INFO_API, {
    method: method,
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

export const getCustomerList = (callback) => {
  return fetch(API.CUSTOMER_LIST_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: Generator.getPostData()
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const updateCustomer = (method, params, callback) => {
  return fetch(API.CUSTOMER_API, {
    method: method,
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