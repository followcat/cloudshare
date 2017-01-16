'use strict';
const webpack = require('webpack');

const folderPath = require('./config/folder-path');
const getHTMLFile = require('./config/html-file');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  output: {
    path: folderPath.PATHS.BUILD_PATH,
    filename: '[name].js',
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"development"',
      },
      __DEVELOPMENT__: true,
    }),
    new ExtractTextPlugin('[name].css'),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
  ].concat(getHTMLFile()),
};
