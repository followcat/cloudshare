require.config({
	baseUrl: "../static/js",

	paths: {
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		header: 'src/header',
		formvalidate: 'src/formvalidate',
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


require(['jquery', 'bootstrap', 'uploadify', 'header', 'formvalidate'], function($, bootstrap, uploadify, header, formvalidate){


});