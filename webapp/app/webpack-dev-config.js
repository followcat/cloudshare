'use strict';
const webpack = require('webpack');
const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const config = require('./config');

module.exports = {
  entry: [
    'babel-polyfill',
    'react-hot-loader/patch',
    `webpack-dev-server/client?http://localhost:${config.port}/`,
    'webpack/hot/only-dev-server',
    './src/index.js'
  ],

  output: {
    path: config.BUILD_PATH,
    publicPath: '/assert/',
    filename: '[name].js',
    chunkFilename: '[name].[chunkhash:5].chunk.js'
  },
  
  devtool: 'cheap-module-eval-source-map',

  devServer: {
    port: config.port,

    inline: true,

    hot: true,

    contentBase: config.BUILD_PATH,

    publicPath: '/assert/',
    
    historyApiFallback: {
      rewrites: [{ from: /^\//, to: '/assert/index.html' }]
    },

    compress: true,

    headers: { 'X-Custom-Foo': 'bar' },

    stats: {
      colors: true,
      chunks: false,
      children: false
    },

    proxy: {
      '/api/*': {
        target: 'http://127.0.0.1:4888',
        secure: false,
      }
    }
  },

  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('dev'),
      },
      __DEVELOPMENT__: true,
    }),
    new ExtractTextPlugin('[name].css'),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
    new HtmlWebpackPlugin({
      hash: false,
      title: 'Cloudshare - Willendare',
      template: path.join(config.SRC_PATH, '/template.html'),
      inject: true
    })
  ]
};
