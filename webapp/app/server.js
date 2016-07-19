const WebpackDevServer = require('webpack-dev-server');
const webpack = require('webpack');
const webpackConf = require('./webpack/webpack.config.js');

const compiler = webpack(webpackConf);

const server = new WebpackDevServer(compiler, {
  //webpack-dev-server options

  contentBase: './app/',

  progress: true,

  inline: true,  //启用inline模式自动刷新

  hot: true,  //启动热加载

  historyApiFallback: true,

  compress: true,  //启用gzip压缩

});

webpackConf.entry.unshift('webpack-dev-server/client?http://0.0.0.0:3000/', 'webpack/hot/only-dev-server');

server.listen(3000, '0.0.0.0', function(err) {
  if (err) {
    console.log(err);
  }
  console.log('Listening at http://0.0.0.0:3000.');
});
