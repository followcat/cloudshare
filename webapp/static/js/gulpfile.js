var gulp = require('gulp');
var Server = require('karma').Server;
var jshint = require('gulp-jshint')

gulp.task('lint', function() {
    return gulp.src('./src/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('jshint-stylish'));
});


/**
 * Run test once and exit
 */
gulp.task('test', function (done) {
  var server = new Server({
  	             configFile: __dirname + '/karma.conf.js',
                 singleRun: true  
             }, function(){ done(); });
  server.start();
});

gulp.task('default', function(){
	gulp.run('lint');

	gulp.watch('./src/*.js', function(){
		gulp.run('lint');
	})
})
