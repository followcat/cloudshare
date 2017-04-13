'use strict';
const WebpackDevServer = require('webpack-dev-server');
const webpack = require('webpack');
const webpackConf = require('./webpack/webpack.config');
const folderPath = require('./webpack/config/folder-path');

const port = 3000;

// 入口加入热加载插件
webpackConf.entry.unshift('react-hot-loader/patch', `webpack-dev-server/client?http://localhost:${port}/`, 'webpack/hot/only-dev-server');

const compiler = webpack(webpackConf);

const server = new WebpackDevServer(compiler, {
  // webpack-dev-server options
  port: port,

  contentBase: folderPath.PATHS.BUILD_PATH,

  inline: true,  // 启用inline模式自动刷新

  hot: true,  // 启动热加载

  // historyApiFallback: true,
  historyApiFallback: {
    rewrites: [{ from: /^\//, to: '/assert/index.html' }]
  },

  compress: true,  //启用gzip压缩

  // It's a required option.
  publicPath: '/assert/',

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
  },

});


server.listen(port, 'localhost', function (err) {
  if (err) {
    console.log(err);
  }
  console.log(`Listening at localhost:${port}.`);
});