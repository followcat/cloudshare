'use strict';
import { API } from 'config/api';
import StorageUtil from 'utils/storage';
import Generator from 'utils/generator';
import { callbackFunction } from './callback';
import 'whatwg-fetch';

export const getHlighLight = (params, callback) => {
  return fetch(API.HIGHLIGHT_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};

export const getHlighLightKeyWord = (params, callback) => {
  return fetch(API.HIGHLIGHT_KEYWORD_API, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(params)
  })
  .then(response => response.json())
  .then(json => callbackFunction(callback, json));
};