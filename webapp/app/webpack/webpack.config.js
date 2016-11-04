'use strict';
const path = require('path');
const fs = require('fs');

const ExtractTextPlugin = require("extract-text-webpack-plugin");
const merge = require('webpack-merge');

const config = require('../config');
const theme = require('../cloudshare-theme-default');

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

let webpackConfig = {
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
        test(filePath) {
          return /\.css$/.test(filePath) && !/\.module\.css$/.test(filePath);
        },
        loader: ExtractTextPlugin.extract(
          'css?sourceMap&-restructuring!' +
          'postcss'
        ),
      },
      {
        test: /\.module\.css$/,
        loader: ExtractTextPlugin.extract(
          'css?sourceMap&-restructuring&modules&localIdentName=[local]___[hash:base64:5]!' +
          'postcss'
        ),
      },
      {
        test(filePath) {
          return /\.less$/.test(filePath) && !/\.module\.less$/.test(filePath);
        },
        loader: ExtractTextPlugin.extract(
          'css?sourceMap!' +
          'postcss!' +
          `less-loader?{"sourceMap":true,"modifyVars":${JSON.stringify(theme)}}`
        ),
      },
      {
        test: /\.module\.less$/,
        loader: ExtractTextPlugin.extract(
          'css?sourceMap&modules&localIdentName=[local]___[hash:base64:5]!!' +
          'postcss!' +
          `less-loader?{"sourceMap":true,"modifyVars":${JSON.stringify(theme)}}`
        ),
      },
      {
        test: /\.(png|jpg)$/,
        loader: 'url?limit=40000',
      },
    ],
  },

  postcss: [require('autoprefixer'), require('precss')],

};


// module.exports = webpackConfig;
if (TARGET === 'start' || !TARGET) {
  module.exports = merge(development, webpackConfig);
}

if (TARGET === 'build' || !TARGET) {
  module.exports = merge(production, webpackConfig);
}