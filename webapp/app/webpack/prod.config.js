'use strict';
const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const config = require('../config');

const HtmlWebpackPlugin = require('html-webpack-plugin');

const getHtml = function() {
  let entryPath = path.resolve(config.PATHS.SRC_PATH, 'entry');
  let dirs = fs.readdirSync(entryPath);
  let matchs = [], htmlFiles = [], eachFile = {};

  dirs.forEach(function(item) {
    matchs = item.match(/(.+)\.entry\.js$/);
    // matchs = item.match(/(^(?!listjd).*)\.entry\.js$/);
    if (matchs) {
      eachFile = new HtmlWebpackPlugin({
        hash: false,
        title: 'Willendare',
        template: path.join(config.PATHS.SRC_PATH, '/template.html'),  // html模板文件
        inject: true,  // 允许修改的内容
        chunks: [matchs[1]],
        filename: path.join(config.PATHS.ROOT_PATH, '/templates_dist/'+ matchs[1] +'.html'),  // 生成的html文件存放路径
        minify: {    // 压缩HTML文件
          removeComments: true,    // 移除HTML中的注释
          collapseWhitespace: false,   // 删除空白符与换行符
        },
      });
      htmlFiles.push(eachFile);
    }
  });
  return htmlFiles;
};

module.exports = {
  output: {
    path: path.join(config.PATHS.STATIC_PATH, '/dist/js'),
    publicPath: '/static/dist/js',
    filename: '[name].bundle[hash].js',
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"',
      },
      __DEVELOPMENT__: false,
    }),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
      },
    }),
  ].concat(getHtml()),
};
