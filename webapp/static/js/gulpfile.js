var gulp = require('gulp'),
    Server = require('karma').Server, //karma服务
    jshint = require('gulp-jshint'),  //js检测
    browserSync = require('browser-sync').create();  //多平台同步

var requirejsOptimize = require('gulp-requirejs-optimize'), //requirejs压缩
    revCollector = require('gulp-rev-collector'); //路径替换

//js错误检测任务
gulp.task('lint', function() {
  return gulp.src('./src/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'));
});

//开启多平台同步服务
gulp.task('browser-sync', function(){
  browserSync.init({
    proxy: "http://0.0.0.0:4888/"
  });
});

//前端测试任务
gulp.task('test', function (done) {
  var server = new Server({
      configFile: __dirname + '/karma.conf.js',
      singleRun: true
    }, function(){ done(); });
  server.start();
});

//默认
gulp.task('default', function(){
  gulp.run('lint');

  gulp.watch('./src/*.js', function(){
    gulp.run('lint');
   });
});
