define(['jquery', 'uploadify', 'formvalidate'], function($, uploadify, formvalidate){

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

	//setting in header
	header.Setting = function(objBtn, objForm, msgBox){
		objBtn.on('click', function(){
			var aPwd = objForm.find(":password");

			if(formvalidate.ValidateBlank(aPwd))
			{
				//change password, send request
				$.ajax({
					url: objForm.attr('action'),
					type: objForm.attr('method'),
					dataType: 'text',
					data: objForm.serialize(),
					success: function(result){
						var resultJson = $.parseJSON(result);
						if(resultJson.result)
						{
							msgBox.text("The password is changed, please login again.");
							setTimeout(function(){
								window.location.href = "/";
							},2000);
						}
						else
						{
							msgBox.text("Operation Failed!");
						}
					},
					error: function(msg){
						alert("Error!");
					}
				});
			}
			event.preventDefault();

		});
	};

	header.Setting($("#cpwd-btn"), $("#cpwd-form"), $("#error-msg"));

	//set button is disable
	header.DisableBtn = function(obj){
		obj.attr("disabled",true);
	}

	//set button is able
	header.AbleBtn = function(obj){
		obj.attr("disabled",false);
	}

	//password input validate
	header.ValidatePwd = function(objOldPwd, objNewPwd, objCfPwd, objCPwdBtn, msgBox){

		//newpassword input validate
		objOldPwd.on('blur', function(){
			if(!formvalidate.ValidatePassword(this.value))
			{
				header.DisableBtn(objCPwdBtn);   //if illegal disable button
				msgBox.text("illegal password. At least 6-12 strings");
			}
			else
			{
				header.AbleBtn(objCPwdBtn);
				msgBox.text("");
			}
		});

		objNewPwd.on('blur', function(){
			if(!formvalidate.ValidatePassword(this.value))
			{
				header.DisableBtn(objCPwdBtn);
				msgBox.text("illegal password. At least 6-12 strings");
			}
			else
			{
				header.AbleBtn(objCPwdBtn);
				msgBox.text("");
			}
		});


		objCfPwd.on('blur', function(){
			var cofpwd = $(this);
			var cofpwdVal = this.value;

			//judge the input value
			if(!formvalidate.ValidatePassword(cofpwdVal))
			{
				header.DisableBtn(objCPwdBtn);
				msgBox.text("illegal confirm password. At least 6-12 strings");
			}
			else
			{
				var pwdVal = $(cofpwd.attr("data-compare")).val();

				if(!formvalidate.ComparePassword(pwdVal, cofpwdVal))
				{
					header.AbleBtn(objCPwdBtn);
					msgBox.text("The passwords you entered do not match. Please re-enter your passwords. ");
				}
				else{
					header.AbleBtn(objCPwdBtn);
					msgBox.text("");
				}
			}	
		});
	};

	header.ValidatePwd($("#oldpassword"), $("#newpassword"), $("#confirmpassword"), $("#cpwd-btn"), $("#error-msg"));

	return header;
});
