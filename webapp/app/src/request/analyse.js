'use strict';
import { API } from 'API';
import { callbackFunction } from './callback';
import Generator from 'utils/generator';
import StorageUtil from 'utils/storage';

import 'whatwg-fetch';

export const getAbilityData = (params, callback) => {
  return fetch(API.MINING_ABILITY_API, {
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

export const getExperienceData = (params, callback) => {
  return fetch(API.MINING_EXPERIENCE_API, {
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

export const getPositionData = (params, callback) => {
  return fetch(API.MINING_POSITION_API, {
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

export const getValuableData = (params, callback) => {
  return fetch(API.MINING_VALUABLE_API, {
    method: 'POST',
    credential: 'include',
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
