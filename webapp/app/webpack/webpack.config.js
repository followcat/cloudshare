'use strict';
const merge = require('webpack-merge');

const getEntryFile = require('./config/entry-file');
const folderPath = require('./config/folder-path');
const theme = require('../cloudshare-theme-default');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

const development = require('./dev.config');
const production = require('./prod.config');

const TARGET = process.env.npm_lifecycle_event;

process.env.BABEL_ENV = TARGET;

let webpackConfig = {
  entry: getEntryFile(),

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
        include: folderPath.PATHS.SRC_PATH,
      },
      {
        test(filePath) {
          return /\.css$/.test(filePath) && !/\.module\.css$/.test(filePath);
        },
        loader: ExtractTextPlugin.extract(
          'style-loader',
          'css-loader?sourceMap&-restructuring!' +
          'postcss-loader'
        ),
      },
      {
        test: /\.module\.css$/,
        loader: ExtractTextPlugin.extract(
          'style-loader',
          'css-loader?sourceMap&-restructuring&modules&localIdentName=[local]___[hash:base64:5]!' +
          'postcss-loader'
        ),
      },
      {
        test(filePath) {
          return /\.less$/.test(filePath) && !/\.module\.less$/.test(filePath);
        },
        loader: ExtractTextPlugin.extract(
          'style-loader',
          'css-loader?sourceMap!' +
          'postcss-loader!' +
          `less-loader?{"sourceMap":true,"modifyVars":${JSON.stringify(theme)}}`
        ),
      },
      {
        test: /\.module\.less$/,
        loader: ExtractTextPlugin.extract(
          'style-loader',
          'css-loader?sourceMap&modules&localIdentName=[local]___[hash:base64:5]!!' +
          'postcss-loader!' +
          `less-loader?{"sourceMap":true,"modifyVars":${JSON.stringify(theme)}}`
        ),
      },
      {
        test: /\.(png|jpg)$/,
        loader: 'url?limit=40000',
      },
    ],
  },

  postcss: [require('autoprefixer')],

};


// module.exports = webpackConfig;
if (TARGET === 'dev' || !TARGET) {
  module.exports = merge(development, webpackConfig);
}

if (TARGET === 'build' || !TARGET) {
  module.exports = merge(production, webpackConfig);
}