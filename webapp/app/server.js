'use strict';
const WebpackDevServer = require('webpack-dev-server');
const webpack = require('webpack');
const webpackConf = require('./webpack/webpack.config');
const config = require('./config');

//遍历每个入口文件并加入热加载插件
let entryObject = webpackConf.entry;
for (let key in entryObject) {
  let arr = [];
  arr.push(entryObject[key]);
  arr.push('webpack-dev-server/client?http://localhost:3000/');
  arr.push('webpack/hot/only-dev-server');
  entryObject[key] = arr;
}

webpackConf.entry = entryObject;
// webpackConf.entry.unshift('webpack-dev-server/client?http://0.0.0.0:4888/', 'webpack/hot/only-dev-server');

const compiler = webpack(webpackConf);

const server = new WebpackDevServer(compiler, {
  // webpack-dev-server options

  contentBase: './',

  progress: true,

  inline: true,  // 启用inline模式自动刷新

  hot: true,  // 启动热加载

  historyApiFallback: true,

  compress: true,  //启用gzip压缩

  // It's a required option.
  publicPath: config.serverConfig.dev.baseURL,

  headers: { "X-Custom-Header": "yes" },

  stats: { colors: true },

  proxy: {
    '/api/*': {
      target: 'http://127.0.0.1:4888',
      secure: false,
    }
  },

});


server.listen(3000, 'localhost', function (err) {
  if (err) {
    console.log(err);
  }
  console.log('Listening at localhost:3000.');
});