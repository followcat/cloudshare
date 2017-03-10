'use strict';
const webpack = require('webpack');
const path = require('path');
const folderPath = require('./config/folder-path');
const getHTMLFile = require('./config/html-file');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  output: {
    path: folderPath.PATHS.BUILD_PATH,
    publicPath: '/assert/',
    filename: '[name].js',
    chunkFilename: '[name].[chunkhash:5].chunk.js'
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
    new HtmlWebpackPlugin({
      hash: false,
      title: 'Cloudshare - Willendare',
      template: path.join(folderPath.PATHS.SRC_PATH, '/template.html'),
      inject: true
    })
  ]
  // ].concat(getHTMLFile()),
};
