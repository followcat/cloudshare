const WebpackDevServer = require('webpack-dev-server');
const webpack = require('webpack');
const webpackConf = require('./webpack/webpack.config.js');

let entryObject = webpackConf.entry;
for (let key in entryObject) {
  let arr = [];
  arr.push(entryObject[key]);
  // arr.push('webpack-dev-server/client?http://localhost:3000/');
  arr.push('webpack/hot/only-dev-server');
  entryObject[key] = arr;
}

entryObject.devServerClient = 'webpack-dev-server/client?http://localhost:3000/';

webpackConf.entry = entryObject;
// webpackConf.entry.unshift('webpack-dev-server/client?http://0.0.0.0:4888/', 'webpack/hot/only-dev-server');
console.log(webpackConf.entry);
const compiler = webpack(webpackConf);

const server = new WebpackDevServer(compiler, {
  // webpack-dev-server options

  contentBase: './app/',

  progress: true,

  inline: true,  // 启用inline模式自动刷新

  hot: true,  // 启动热加载

  historyApiFallback: true,

  compress: true,  //启用gzip压缩

});


server.listen(3000, 'localhost', function (err) {
  if (err) {
    console.log(err);
  }
  console.log('Listening at localhost:3000.');
});