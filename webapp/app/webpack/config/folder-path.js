'use strict';
const path = require('path');

module.exports = {
  PATHS: {
    ROOT_PATH: path.join(__dirname, '../../../'),
    APP_PATH: path.join(__dirname, '../../'),
    SRC_PATH: path.join(__dirname, '../../src'),
    BUILD_PATH: path.join(__dirname, '../../build'),
    LIB_PATH: path.join(__dirname, '../../lib'),
    STATIC_PATH: path.join(__dirname, '../../../static'),
    NODE_MODULES_PATH: path.join(__dirname, '../../node_modules'),
  },
};