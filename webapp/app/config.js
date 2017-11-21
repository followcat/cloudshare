'use strict';
const path = require('path');

module.exports = {
  port: 3000,

  SRC_PATH: path.join(__dirname, 'src'),

  BUILD_PATH: path.join(__dirname, 'build'),

  STATIC_PATH: path.join(__dirname, '../static'),

  PROD_STATIC_PATH: path.join(__dirname, '../static.prod'),

  ROOT_PATH: path.join(__dirname, '../')
};
