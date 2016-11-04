var gulp = require('gulp'),
    Server = require('karma').Server, //karma服务
    jshint = require('gulp-jshint'),  //js检测
    browserSync = require('browser-sync').create();  //多平台同步

var requirejsOptimize = require('gulp-requirejs-optimize'), //requirejs压缩
    revCollector = require('gulp-rev-collector'), //路径替换
    rev = require('gulp-rev'),  //文件名加md5后缀
    minifyHTML = require('gulp-minify-html'),  //html压缩优化
    clean = require('gulp-clean'),  //文件夹清空
    cleanCSS = require('gulp-clean-css');  //压缩CSS

//清除构建文件夹
gulp.task("clean", function(){
  return gulp.src(["./dist/js/", "./dist/css/", "../templates_dist/"])
    .pipe(clean({force: true}));
})

//js打包任务
gulp.task('scripts', function(){
  // return gulp.src(["src/js/modules/*.js",
  //                 "!src/js/modules/batchupload.js",
  //                 "!src/js/modules/index.js",
  //                 "!src/js/modules/urm_home.js",
  //                 "!src/js/modules/urm_setting.js",
  //                 "!src/js/modules/search.js"])
  return gulp.src([
      // "src/js/modules/cvsource.js",
      // "src/js/modules/edit.js",
      // "src/js/modules/modify.js",
    ])
    .pipe(requirejsOptimize({
      paths: {
        jquery: __dirname + '/lib/js/jquery',
        bootstrap: __dirname + '/lib/js/bootstrap',
        marked: __dirname + '/lib/js/marked',
        fileuploader: __dirname + '/lib/js/jquery.uploadfile.min',
        bootstraptable: __dirname + '/lib/js/bootstrap-table.min',
        datetimepicker: __dirname + '/lib/js/bootstrap-datetimepicker.min',
        datetimepickerCN: __dirname + '/lib/js/bootstrap-datetimepicker.zh-CN',
        cvdeal: __dirname + '/src/js/util/cv_deal',
        header: __dirname + '/src/js/util/header',
        formvalidate: __dirname + '/src/js/util/formvalidate',
        Upload: __dirname + '/src/js/util/upload',
        History: __dirname + '/src/js/util/history',
        radarcharts: __dirname + '/src/js/util/charts/radarcharts',
        barcharts: __dirname + '/src/js/util/charts/barcharts',
        scatters: __dirname + '/src/js/util/charts/scattercharts',
        colorgrad: __dirname + '/src/js/util/colorgrad',
        urmmain: __dirname + '/src/js/util/urm_main',
        ChartsCommon: __dirname + '/src/js/util/charts/charts_common',
        ProcessInfo: __dirname + '/src/js/util/process_info'
      },
      shim: {
        bootstrap: {
          deps: ['jquery'],
          exports: 'bootstrap'
        },
        bootstraptable: {
          deps: ['jquery'],
          exports: 'bootstraptable'
        },
        marked: {
          exports: 'marked'
        },
        shim: {
          cvdeal: {
            deps: ['jquery'],
            exports: 'cvdeal'
          }
        }
      }
    }))
    .pipe(rev())
    .pipe(gulp.dest("dist/js"))
    .pipe(rev.manifest())
    .pipe(gulp.dest("rev/js"))
});

//css打包任务
gulp.task("style", function(){
  return gulp.src("src/css/*.css")
    .pipe(cleanCSS({ keepSpecialComments: 1, processImport: false }))
    .pipe(rev())
    .pipe(gulp.dest("dist/css"))
    .pipe(rev.manifest())
    .pipe(gulp.dest("rev/css"))
});

//路径替换
gulp.task("rev", ["scripts", "style"], function(){
  return gulp.src(["./rev/**/*.json",
                  "../templates/**/*.html",
                  "!../templates/batchupload.html",
                  "!../templates/companyview.html",
                  "!../templates/index.html",
                  "!../templates/jdview.html",
                  "!../templates/lsipage.html",
                  "!../templates/makechart.html",
                  "!../templates/search.html",
                  "!../templates/serach_result.html",
                  "!../templates/upload_preview.html",
                  "!../templates/cv_refactor.html"])
    .pipe(revCollector({
      replaceReved: true,
      dirReplacements: {
        "src/js/modules": "dist/js",
        "src/css": "dist/css"
      }
    }))
    .pipe(gulp.dest("../templates_dist/"))
});

gulp.task("build", ["scripts", "style", "rev"]);

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
      configFile: __dirname + 'js/karma.conf.js',
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
