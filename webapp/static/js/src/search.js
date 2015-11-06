require.config({
	baseUrl: "../static/js",

	paths: {
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		header: 'src/header',
		formvalidate: 'src/formvalidate',
		Upload: 'src/upload'
	},
	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		}
	}
});


require(['jquery', 'bootstrap', 'header', 'formvalidate', 'Upload'], function($, bootstrap, header, formvalidate, Upload){


});