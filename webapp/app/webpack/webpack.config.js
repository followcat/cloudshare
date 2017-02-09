'use strict';
const webpack = require('webpack');
const merge = require('webpack-merge');
const path = require('path');

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

  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      'components': path.resolve(folderPath.PATHS.SRC_PATH, 'components/'),
      'views': path.resolve(folderPath.PATHS.SRC_PATH, 'views/'),
      'utils': path.resolve(folderPath.PATHS.SRC_PATH, 'utils/'),
      'request': path.resolve(folderPath.PATHS.SRC_PATH, 'request/'),
      'config': path.resolve(folderPath.PATHS.SRC_PATH, 'config/'),
      'API': path.resolve(folderPath.PATHS.SRC_PATH, 'config/api.js'),
      'URL': path.resolve(folderPath.PATHS.SRC_PATH, 'config/url.js')
    }
  },

  module: {
    rules: [{
      test: /\.js|jsx$/,
      exclude: /node_modules/,
      use: ['babel-loader'],
      include: folderPath.PATHS.SRC_PATH,
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
    // new webpack.DllReferencePlugin({
    //   context: __dirname,
    //   manifest: require('../lib/vendor-manifest.json')
    // }),
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