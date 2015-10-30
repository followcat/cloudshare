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
			'onUploadProgress' : function(file, bytesUploaded, bytesTotal, totalBytesUploaded, totalBytesTotal) {
	            $('#progress').html(totalBytesUploaded + ' bytes uploaded of ' + totalBytesTotal + ' bytes.');
	        },
			'onUploadError' : function(file, errorCode, errorMsg, errorString) {   //upload fail ,catch the error info
	            alert('The file ' + file.name + ' could not be uploaded: ' + errorString);
	        },
	        'onUploadSuccess' : function(file, data, response) {                //upload success event 
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

	return header;
});
