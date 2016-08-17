'use strict';
const path = require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const merge = require('webpack-merge');

const development = require('./dev.config');
const production = require('./prod.config');

const TARGET = process.env.npm_lifecycle_event;

process.env.BABEL_ENV = TARGET;

const PATHS = {
  ROOT_PATH: path.join(__dirname, '../'),
  SRC_PATH: path.join(__dirname, '../src'),
  BUILD_PATH: path.join(__dirname, '../dist'),
};

const getEntry = function() {
  let entryPath = path.resolve(PATHS.SRC_PATH, 'entry');
  let dirs = fs.readdirSync(entryPath);
  let matchs = [], files = {};
  dirs.forEach(function(item) {
    matchs = item.match(/(.+)\.entry\.js$/);
    if (matchs) {
      files[matchs[1]] = path.resolve(PATHS.SRC_PATH, 'entry', item);
    }
  });
  return files;
};

const getHtml = function() {
  let entryPath = path.resolve(PATHS.SRC_PATH, 'entry');
  let dirs = fs.readdirSync(entryPath);
  let matchs = [], htmlFiles = [], eachFile = {};

  dirs.forEach(function(item) {
    matchs = item.match(/(.+)\.entry\.js$/);
    console.log(matchs);
    if (matchs) {
      eachFile = new HtmlWebpackPlugin({
        template: path.join(PATHS.SRC_PATH, '/template.html'),  // html模板文件
        inject: true,  // 允许修改的内容
        filename: path.join(PATHS.BUILD_PATH, '/'+ matchs[1] +'.html'),  // 生成的html文件存放路径
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

const config = {
  entry: getEntry(),

  output: {
    path: PATHS.BUILD_PATH,
    filename: '[name].bundle[hash].js',
  },

  resolve: {
    extensions: ['', '.js', '.jsx'],
  },

  module: {
    loaders: [
      {
        test: /\.js|jsx$/,
        exclude: /node_modules/,
        loaders: ['react-hot', 'babel'],
        include: PATHS.SRC_PATH,
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader?modules',
        include: PATHS.SRC_PATH,
      },
      {
        test: /\.(png|jpg)$/,
        loader: 'url?limit=40000',
      },
    ],
  },

  plugins: getHtml(),
};

// module.exports = config;
if (TARGET === 'start' || !TARGET) {
  module.exports = merge(development, config);
}

if (TARGET === 'build' || !TARGET) {
  module.exports = merge(production, config);
}