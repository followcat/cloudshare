var gulp = require('gulp');
// var jshint = require('gulp-jshint');
var karma = require('gulp-karma');

// gulp.task('lint',function(){
// 	return gulp.src('js/*.js')
// 	  .pipe(jshint())
// 	  .pipe(jshint.reporter('jshint-stylish'));

// });


//gulp-karma task
gulp.task('test',function(){
	return gulp.src(['test/*.js'])
	  .pipe(karma({
	  	configFile: 'karma.conf.js',
	  	action: 'run'
	  }));
});

// gulp.task('watch', function(){
// 	gulp.watch('js/*.js',['lint']);
// });