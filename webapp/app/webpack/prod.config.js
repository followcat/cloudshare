'use strict';
const path = require('path');
const webpack = require('webpack');

const getHTMLFile = require('./config/html-file');
const folderPath = require('./config/folder-path');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  output: {
    path: path.join(folderPath.PATHS.STATIC_PATH, '/dist'),
    publicPath: '/static/dist',
    filename: '[name].[hash].js',
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
      filename: '[name].[contenthash].css',
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
    })
  ].concat(getHTMLFile()),

  stats: {
    color: true,
    chunks: false,
    children: false
  },
};
