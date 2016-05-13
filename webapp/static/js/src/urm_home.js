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

require(['jquery', 'bootstrap', 'urmmain','formvalidate'],function($, bootstrap, urmmain,formvalidate){
	// body...
	var msgBox = $(".error-msg");

	//set up the button of save to open or close
	var saveBtn = $("#save-btn");

	//Add User button event
	saveBtn.on('click', function(event){
		//get the form
		var aForm = $("#add-user-form");

		var aText = aForm.find(":text");
		var aPwd = aForm.find(":password");

		if( !formvalidate.ValidateBlank(aText) && !formvalidate.ValidateBlank(aPwd))
		{
			//call the ajax request
			urmmain.FormAjax(aForm, function(){

				alert("Successful Add!");
				window.location.reload();

			}, function(){
				$("#addUserName").focus();

			});
		}


		event.preventDefault();
	});

	//validate user name form
	$("#addUserName").on('blur', function(){
		var userName = this.value;

		if(!formvalidate.ValidateAccount(userName))
		{
			urmmain.ButtonDisable(saveBtn);
			msgBox.text("illegal account");
		}
		else{
			urmmain.ButtonAble(saveBtn);
			msgBox.text("");
		}
	});

	//validate password form
	$("#password").on('blur', function(){
		var pwd = this.value;

		if(!formvalidate.ValidatePassword(pwd))
		{
			urmmain.ButtonDisable(saveBtn);
			msgBox.text("illegal password. At least 6-12 strings");
		}
		else{
			urmmain.ButtonAble(saveBtn);
			msgBox.text("");
		}

	});

	//validate confirm password form
	$("#confirmPassword").on('blur', function(){

		//get the confirm password
		var cofpwd = $(this);
		var cofpwdVal = cofpwd.val();

		//judge the input value
		if(!formvalidate.ValidatePassword(cofpwdVal))
		{
			urmmain.ButtonDisable(saveBtn);
			msgBox.text("illegal confirm password. At least 6-12 strings");
		}
		else
		{
			var pwdVal = $(cofpwd.attr("data-compare")).val();

			if(!formvalidate.ComparePassword(pwdVal, cofpwdVal))
			{
				urmmain.ButtonDisable(saveBtn);
				msgBox.text("The passwords you entered do not match. Please re-enter your passwords. ");
			}
			else{
				urmmain.ButtonAble(saveBtn);
				msgBox.text("");
			}
		}
	});


	//Delete Button
	$("table tbody button").on('click', function(){
		var trParent = $(this).parent().parent();
		var deletename = trParent.find(".name").text();

		if(confirm("Are you sure to delete " + deletename + "?"))
		{
			$.ajax({
				url: '/deleteuser',
				type: 'POST',
				data: "name="+deletename,
				dataType: 'text',
				success: function(result){
					alert("Successful Delete!");
					window.location.reload();
				}

			});
		}
	});
});
