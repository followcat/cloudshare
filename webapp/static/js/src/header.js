define(['jquery', 'uploadify'], function($, uploadify){

	var header = {};


	//upload modal, button of choose file config
	header.upload = function(){
		$("#uploadify").uploadify({
			'swf': 'static/js/plugin/uploadify/uploadify.swf',
			'uploader': '/upload',
			'buttonText': 'Choose File',
			'progressData': 'percentage',
			'queueID': false,
			'auto': false,         //automatically upload
			'multi': false,        //multiple files
			'onUploadStart': function(file){
					$("#uploading").show();
			},
			'onSelect': function(file){
					$("#uploading").hide();
					$("#upload-success").hide();
					$("#upload-fail").hide();
			},
			'onUploadProgress' : function(file, fileBytesLoaded, fileTotalBytes) {
	            $('#progress').html(fileBytesLoaded + ' bytes uploaded of ' + fileTotalBytes + ' bytes.');
	    },
			'onUploadError' : function(file, errorCode, errorMsg) {   //upload fail ,catch the error info
	            alert('The file ' + file.name + ' could not be uploaded: ' + errorMsg);
	    },
	    'onUploadSuccess' : function(file, data, response) {                //upload success event 
	    	console.log();
	      if(response)
	      {
	      	$("#uploading").hide();
	      	$("#upload-success").show();

	        setTimeout(function(){
	        	window.location.href = '/uppreview';
	        },2000);
	      }
	      else
	      {
	      	$("#uploading").hide();
	      	$("#upload-fail").show();
	      }
	    }
		});
	};
	header.upload();

	header.UploadHandle = function(btnObj){	
		$(btnObj).on('click', function(){
			$("#uploadify").uploadify('upload');
		});
	};

	header.UploadHandle("#upload-btn");

	// Login out in header
	header.LogOut = function(obj){
		//obj is a element object
		obj.on("click", function(event){

			$.ajax({
				url: '/logout',
				type: 'GET',
				success: function(){
					window.location.href = "/";
				},
				error: function(msg){
					alert("Operate Error!");
				}

			});

			event.preventDefault();    //prevent event default.
		});

	};

	header.LogOut($("#quit-btn"));

	header.UploadDiv = function(obj){
		obj.on('click', function(){
			$("#uploading").hide();
			$("#upload-success").hide();
			$("#upload-fail").hide();
		});
	};

	header.UploadDiv($(".upload"));

	return header;
});
