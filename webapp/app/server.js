'use strict';
const WebpackDevServer = require('webpack-dev-server');
const webpack = require('webpack');
const webpackConf = require('./webpack/webpack.config');

//遍历每个入口文件并加入热加载插件
let entryObject = webpackConf.entry;
for (let key in entryObject) {
  let arr = [];
  arr.push('react-hot-loader/patch');
  arr.push('webpack-dev-server/client?http://localhost:3000/');
  arr.push('webpack/hot/only-dev-server');
  arr.push(entryObject[key]);
  entryObject[key] = arr;
}

webpackConf.entry = entryObject;
// webpackConf.entry.unshift('webpack-dev-server/client?http://0.0.0.0:4888/', 'webpack/hot/only-dev-server');

const compiler = webpack(webpackConf);

const port = 3000;

const server = new WebpackDevServer(compiler, {
  // webpack-dev-server options

  contentBase: './',

  inline: true,  // 启用inline模式自动刷新

  hot: true,  // 启动热加载

  historyApiFallback: true,

  compress: true,  //启用gzip压缩

  // It's a required option.
  publicPath: `http://localhost:${port}/`,

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