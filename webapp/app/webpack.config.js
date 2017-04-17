'use strict';
const webpack = require('webpack');
const merge = require('webpack-merge');
const path = require('path');

// const folderPath = require('./config/folder-path');
const theme = require('./cloudshare-theme-default');
const config = require('./config');

const ExtractTextPlugin = require('extract-text-webpack-plugin');

const development = require('./webpack-dev-config');
const production = require('./webpack-prod-config');

const TARGET = process.env.npm_lifecycle_event;

process.env.BABEL_ENV = TARGET;

let webpackConfig = {

  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      'components': path.resolve(config.SRC_PATH, 'components/'),
      'routes': path.resolve(config.SRC_PATH, 'routes/'),
      'views': path.resolve(config.SRC_PATH, 'views/'),
      'utils': path.resolve(config.SRC_PATH, 'utils/'),
      'request': path.resolve(config.SRC_PATH, 'request/'),
      'config': path.resolve(config.SRC_PATH, 'config/'),
      'API': path.resolve(config.SRC_PATH, 'config/api.js'),
      'URL': path.resolve(config.SRC_PATH, 'config/url.js'),
      'image': path.resolve(config.SRC_PATH, 'image/')
    }
  },

  module: {
    rules: [{
      test: /\.js|jsx$/,
      exclude: /node_modules/,
      use: ['babel-loader'],
      include: config.SRC_PATH,
    }, {
      test: '/\.css$/',
      exclude: /node_modules/,
      loader: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: ['css-loader', 'postcss-loader']
      })
    }, {
      test: /\.less$/i,
      loader: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: ['css-loader', 'postcss-loader' ,`less-loader?{"modifyVars":${JSON.stringify(theme)}}`]
      })
    }, {
      test: /\.(png|jpg)$/,
      exclude: /node_modules/,
      use: 'url-loader?limit=40000',
    }]
  },
  
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: 'commons'
    })
  ]
};

// module.exports = webpackConfig;
if (TARGET === 'dev' || !TARGET) {
  module.exports = merge(development, webpackConfig);
}

if (TARGET === 'build' || !TARGET) {
  module.exports = merge(production, webpackConfig);
}