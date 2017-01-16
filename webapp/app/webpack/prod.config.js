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
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"',
      },
      __DEVELOPMENT__: false,
    }),
    new ExtractTextPlugin('[name].[hash].css', {
      allChunks: true,
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'commons'
    }),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
      },
    }),
  ].concat(getHTMLFile()),
};
