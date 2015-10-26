var gulp = require('gulp');
var Server = require('karma').Server;

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
