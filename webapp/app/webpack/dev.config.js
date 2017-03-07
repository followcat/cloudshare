'use strict';
const webpack = require('webpack');

const folderPath = require('./config/folder-path');
const getHTMLFile = require('./config/html-file');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  output: {
    path: folderPath.PATHS.BUILD_PATH,
    publicPath: '/assert/',
    filename: '[name].js',
  },
  
  devtool: 'cheap-module-eval-source-map',

  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('dev'),
      },
      __DEVELOPMENT__: true,
    }),
    new ExtractTextPlugin('[name].css'),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
  ].concat(getHTMLFile()),
};
