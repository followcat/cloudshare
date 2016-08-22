'use strict';
const path = require('path');

module.exports = {
  host: "http://0.0.0.0:4888",
  serverConfig: {
    dev: {
      baseURL: 'http://localhost:3000/',
    },
    prod: {
      baseURL: 'http://0.0.0.0:4888/webapp',
    },
    test: {},
  },
  PATHS: {
    ROOT_PATH: path.join(__dirname, '../'),
    APP_PATH: path.join(__dirname, './'),
    SRC_PATH: path.join(__dirname, './src'),
    BUILD_PATH: path.join(__dirname, './dist'),
    STATIC_PATH: path.join(__dirname, '../static'),
  },
};