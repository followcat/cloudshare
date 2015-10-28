require.config({
	baseUrl: "../static/js",

	paths: {
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		header: 'src/header',
		uploadify: 'plugin/uploadify/uploadify'
	},
	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		},
		uploadify: {
			deps: ['jquery'],
			exports: 'uploadify'
		}
	}
});


require(['jquery', 'bootstrap', 'uploadify', 'header'], function($, bootstrap, uploadify, header){


});