require.config({
	baseUrl: '../static/js',
	paths:{
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		formvalidate: 'src/formvalidate',
		urmmain: 'src/urm_main'
	},
	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		}
	}
});

require(['jquery', 'bootstrap', 'urmmain', 'formvalidate'],function($, bootstrap, urmmain, formvalidate){
	// body...
	
	var msgBox = $(".error-msg");
	var submitBtn = $("#submit-btn");

	//change password click event
	submitBtn.on('click', function(event){
		var aForm = $("#settin-form");

		var aPwd = aForm.find(":password");

		if(!formvalidate.ValidateBlank(aPwd))
		{
			urmmain.FormAjax(aForm, function(){
				alert("The password is changed, please login again.");
				window.location.href = "/";

			}, function(){
				$("#oldpassword").focus();
			});
		}
		event.preventDefault();
	});

	//validate the password form
	function PasswordValidate(objVal){
		if(!formvalidate.ValidatePassword(objVal))
		{
			urmmain.ButtonDisable(submitBtn);
			msgBox.text("illegal password. At least 6-12 strings");
		}
		else{
			urmmain.ButtonAble(submitBtn);
			msgBox.text("");
		}
	}

	$("#oldpassword").on('blur', function(){
		PasswordValidate(this.value);
	});

	$("#newpassword").on('blur', function(){
		PasswordValidate(this.value);
	});


	$("#confirmpassword").on('blur', function(){
		var cofpwd = $(this);
		var cofpwdVal = this.value;

		//judge the input value
		if(!formvalidate.ValidatePassword(cofpwdVal))
		{
			urmmain.ButtonDisable(submitBtn);
			msgBox.text("illegal confirm password. At least 6-12 strings");
		}
		else
		{
			var pwdVal = $(cofpwd.attr("data-compare")).val();

			if(!formvalidate.ComparePassword(pwdVal, cofpwdVal))
			{
				urmmain.ButtonDisable(submitBtn);
				msgBox.text("The passwords you entered do not match. Please re-enter your passwords. ");
			}
			else{
				urmmain.ButtonAble(submitBtn);
				msgBox.text("");
			}
		}	
	});

});
