'use strict';
const path = require('path'),
      fs = require('fs'),
      folderPath = require('./folder-path');

const HtmlWebpackPlugin = require('html-webpack-plugin');

const env = process.env.npm_lifecycle_event;

const getHTMLFile = function() {
  let entryPath = path.resolve(folderPath.PATHS.SRC_PATH, 'entry'),
      dirs = fs.readdirSync(entryPath),
      matchs = [], htmlFiles = [], eachFile = {};

  dirs.forEach(function(item) {
    matchs = item.match(/(.+)\.entry\.js$/);
    if (matchs) {
      eachFile = new HtmlWebpackPlugin({
        hash: false,
        title: 'Cloudshare - Willendare',
        template: path.join(folderPath.PATHS.SRC_PATH, '/template.html'),  // html模板文件
        inject: true,  // 允许修改的内容
        chunks: [matchs[1], 'commons'],
        chunksSortMode: 'dependency',
        filename: function (filename) {
          if (env === 'dev') {
            return path.join(folderPath.PATHS.BUILD_PATH, '/'+ filename +'.html');
          } else {
            return path.join(folderPath.PATHS.ROOT_PATH, '/templates_dist/'+ filename +'.html');
          }
        }(matchs[1]),  // 生成的html文件存放路径
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

module.exports = getHTMLFile;
