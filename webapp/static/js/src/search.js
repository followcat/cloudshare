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

	//logout
	header.LogOut($("#quit-btn"));


	//jquery plugin - uploadify  config
	$("#uploadify").uploadify({
		'swf': 'static/js/plugin/uploadify/uploadify.swf',
		'uploader': '/upload',
		'buttonText': 'Choose File',
		'auto': false,         //automatically upload
		'multi': false,        //multiple files
		'onUploadError' : function(file, errorCode, errorMsg, errorString) {   //upload fail ,catch the error info
            alert('The file ' + file.name + ' could not be uploaded: ' + errorString);
        },
        'onUploadSuccess' : function(file, data, response) {                //upload success event 
            console.log("response: " + response);
            console.log("data: " + data);
            if(response)
            {
            	alert('The file ' + file.name + ' was successfully uploaded ');
            	window.location.href = '/uppreview';
            }
            else
            {
            	alert('The file ' + file.name + ' was failed uploaded ');
            }
        }
	});


	$("#upload-btn").on('click', function(){
		$("#uploadify").uploadify('upload');
	})
});