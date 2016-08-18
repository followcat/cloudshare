'use strict';
const path = require('path');
const fs = require('fs');
// const HtmlWebpackPlugin = require('html-webpack-plugin');
const merge = require('webpack-merge');

const config = require('../config');

const development = require('./dev.config');
const production = require('./prod.config');

const TARGET = process.env.npm_lifecycle_event;

process.env.BABEL_ENV = TARGET;

const getEntry = function() {
  let entryPath = path.resolve(config.PATHS.SRC_PATH, 'entry');
  let dirs = fs.readdirSync(entryPath);
  let matchs = [], files = {};
  dirs.forEach(function(item) {
    matchs = item.match(/(.+)\.entry\.js$/);
    if (matchs) {
      files[matchs[1]] = path.resolve(config.PATHS.SRC_PATH, 'entry', item);
    }
  });
  return files;
};

const webpackConfig = {
  entry: getEntry(),

  // output: {},

  resolve: {
    extensions: ['', '.js', '.jsx'],
  },

  module: {
    loaders: [
      {
        test: /\.js|jsx$/,
        exclude: /node_modules/,
        loaders: ['react-hot', 'babel'],
        include: config.PATHS.SRC_PATH,
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader?modules',
      },
      {
        test: /\.less$/,
        loader: "style!css!less"
      },
      {
        test: /\.(png|jpg)$/,
        loader: 'url?limit=40000',
      },
    ],
  },

};


// module.exports = webpackConfig;
if (TARGET === 'start' || !TARGET) {
  module.exports = merge(development, webpackConfig);
}

if (TARGET === 'build' || !TARGET) {
  module.exports = merge(production, webpackConfig);
}