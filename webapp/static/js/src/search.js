require.config({
	baseUrl: "../static/js",

	paths: {
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		header: 'src/header'
	},
	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		}
	}
});


require(['jquery', 'bootstrap', 'header'], function($,bootstrap,header){
	//upload modal, button of choose file config
	header.UploadChooseFile($("#choose-file-btn"),$("#file-text"));

	//logout
	header.LogOut($("#quit-btn"));
	
});