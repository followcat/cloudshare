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

/**
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

/**
 * 获取待开发客户列表
 * @param  {string}   params   请求参数: 公司名称关键词
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getAddedCompanyList = (params, callback) => {
  return fetch(API.ADDED_COMPANY_LIST_API, {
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

/**
 * 获取公司列表搜索结果
 * @param  {object}   params   请求参数: 页码, 每页条数, 搜索关键字
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const getAllCompanyBySearch = (params, callback) => {
  return fetch(API.COMPANY_BY_SEARCH_KEY_API, {
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

/**
 * 更新公司信息
 * @param  {object}   params   需要更新的字段参数
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const updateCompanyInfo = (params, callback) => {
  return fetch(API.UPDATE_COMPANY_INFO_API, {
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
  .then(json => callbackFunction(callback, json));
};

/**
 * 获取客户公司列表
 * @param {function} callback  回调函数
 */
export const getCustomerList = (callback) => {
  return fetch(API.COMPANY_CUSTOMER_LIST_API, {
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

/**
 * 更新客户信息
 * @param {string} method 异步请求方法
 * @param {object} params 请求参数
 * @param {function} callback 回调函数
 */
export const updateCustomer = (method, params, callback) => {
  return fetch(API.COMPANY_CUSTOMER_API, {
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

/**
 * 确认公司excel文件上传
 * @param {object} params 请求参数
 * @param {function} callback 回调函数
 */
export const confirmExcelUpload = (params, callback) => {
  return fetch(API.CONFIRM_UPLOAD_EXCEL_API, {
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
  .then(json => callbackFunction(callback, json));
};