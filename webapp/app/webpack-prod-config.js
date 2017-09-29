'use strict';
const webpack = require('webpack');
const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const config = require('./config');

module.exports = {
  entry: [
    'babel-polyfill',
    './src/index.js'
  ],

  output: {
    path: config.PROD_STATIC_PATH,
    publicPath: '/static/',
    filename: 'js/[name].[hash].js',
  },

  plugins: [
    new webpack.LoaderOptionsPlugin({
        minimize: true,
        debug: false
    }),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      },
      __DEVELOPMENT__: false,
    }),
    new ExtractTextPlugin({
      filename: 'css/[name].[contenthash].css',
      allChunks: true
    }),
    new webpack.optimize.UglifyJsPlugin({
      beautify: false,
        mangle: {
          screw_ie8: true,
          keep_fnames: true
        },
        compress: {
          screw_ie8: true,
          warnings: false
        },
        comments: false
    }),
    new HtmlWebpackPlugin({
      hash: false,
      title: 'Cloudshare - Willendare',
      template: path.join(config.SRC_PATH, '/template.html'),
      inject: true,
      filename: path.join(config.ROOT_PATH, '/templates_dist.prod/index.html'),
      minify: {    // 压缩HTML文件
        removeComments: true,    // 移除HTML中的注释
        collapseWhitespace: false,   // 删除空白符与换行符
      }
    })
  ],  

  stats: {
    color: true,
    chunks: false,
    children: false
  },
};
