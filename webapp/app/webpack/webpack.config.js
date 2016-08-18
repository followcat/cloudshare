'use strict';
const path = require('path');
const fs = require('fs');
// const HtmlWebpackPlugin = require('html-webpack-plugin');
const merge = require('webpack-merge');

const config = require('../config');

const development = require('./dev.config');
const production = require('./prod.config');

const TARGET = process.env.npm_lifecycle_event;

process.env.BABEL_ENV = TARGET;

const getEntry = function() {
  let entryPath = path.resolve(config.PATHS.SRC_PATH, 'entry');
  let dirs = fs.readdirSync(entryPath);
  let matchs = [], files = {};
  dirs.forEach(function(item) {
    matchs = item.match(/(.+)\.entry\.js$/);
    if (matchs) {
      files[matchs[1]] = path.resolve(config.PATHS.SRC_PATH, 'entry', item);
    }
  });
  return files;
};

// const getHtml = function() {
//   let entryPath = path.resolve(config.PATHS.SRC_PATH, 'entry');
//   let dirs = fs.readdirSync(entryPath);
//   let matchs = [], htmlFiles = [], eachFile = {};

//   dirs.forEach(function(item) {
//     matchs = item.match(/(.+)\.entry\.js$/);
//     if (matchs) {
//       eachFile = new HtmlWebpackPlugin({
//         hash: false,
//         title: 'Willendare',
//         template: path.join(config.PATHS.SRC_PATH, '/template.html'),  // html模板文件
//         inject: true,  // 允许修改的内容
//         chunks: [matchs[1]],
//         filename: path.join(config.PATHS.BUILD_PATH, '/'+ matchs[1] +'.html'),  // 生成的html文件存放路径
//         minify: {    // 压缩HTML文件
//           removeComments: true,    // 移除HTML中的注释
//           collapseWhitespace: false,   // 删除空白符与换行符
//         },
//       });
//       htmlFiles.push(eachFile);
//     }
//   });
//   return htmlFiles;
// };

const webpackConfig = {
  entry: getEntry(),

  // output: {
  //   path: config.PATHS.BUILD_PATH,
  //   filename: '[name].bundle.js',
  // },

  resolve: {
    extensions: ['', '.js', '.jsx'],
  },

  module: {
    loaders: [
      {
        test: /\.js|jsx$/,
        exclude: /node_modules/,
        loaders: ['react-hot', 'babel'],
        include: config.PATHS.SRC_PATH,
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader?modules',
        include: config.PATHS.SRC_PATH,
      },
      {
        test: /\.(png|jpg)$/,
        loader: 'url?limit=40000',
      },
    ],
  },

  // plugins: getHtml(),

};


// module.exports = webpackConfig;
if (TARGET === 'start' || !TARGET) {
  module.exports = merge(development, webpackConfig);
}

if (TARGET === 'build' || !TARGET) {
  module.exports = merge(production, webpackConfig);
}