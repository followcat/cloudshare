'use strict';
import StorageUtil from 'utils/storage';
import Generator from 'utils/generator';
import { API } from 'config/api';
import { newFetch } from './newfetch';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

// 获取公司信息
export const getCompanyInfo = (params, callback) => {
  return newFetch(`${API.COMPANY_API}/${params.id}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 获取简历中公司信息
export const getResumeCompanyInfo = (params, callback) => {
  return newFetch(`${API.RESUME_COMPANY_API}/${params.id}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

// 搜索公司
export const searchCompany = (params, callback) => {
  return fetch(`${API.SEARCH_COMPANY_API}?${params.param}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Authorization': `Basic ${StorageUtil.get('token')}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

/**
 * 获取客户公司列表
 * @param  {fucntion} callback [description]
 * @return {fucntion}            [description]
 */
export const getCompanys = (callback) => {
  return newFetch(API.COMPANYLIST_API, {
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
  return newFetch(API.COMPANY_API, {
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
  return newFetch(API.ALL_COMPANY_API, {
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
  return newFetch(API.ADDED_COMPANY_LIST_API, {
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
  return newFetch(API.COMPANY_BY_SEARCH_KEY_API, {
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
  return newFetch(API.UPDATE_COMPANY_INFO_API, {
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
  .then(json => callbackFunction(callback, json));
};

/**
 * 更新公司信息List
 * @param  {object}   params   需要更新的字段参数
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const updateCompanyInfoList = (params, callback) => {
  return newFetch(API.UPDATE_COMPANY_INFO_API, {
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
 * 删除公司信息List
 * @param  {object}   params   需要更新的字段参数
 * @param  {function} callback 回调函数
 * @return {function} fetch    异步请求方法
 */
export const deleteCompanyInfoList = (params, callback) => {
  return newFetch(API.UPDATE_COMPANY_INFO_API, {
    method: 'DELETE',
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
export const getCustomerList = (params,callback) => {
  return newFetch(API.COMPANY_CUSTOMER_LIST_API, {
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
 * 更新客户信息
 * @param {string} method 异步请求方法
 * @param {object} params 请求参数
 * @param {function} callback 回调函数
 */
export const updateCustomer = (method, params, callback) => {
  return newFetch(API.COMPANY_CUSTOMER_API, {
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
  return newFetch(API.CONFIRM_UPLOAD_EXCEL_API, {
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