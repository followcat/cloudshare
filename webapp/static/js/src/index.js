require.config({
	baseUrl: "../static/js",

	paths: {
		jquery: 'lib/jquery',
		formvalidate: 'src/formvalidate',
		bootstrap: 'lib/bootstrap',
		marked: 'lib/marked'
	},

	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		},
		marked: {
			exports: 'marked'
		}
	}
});

require(['jquery', 'formvalidate', 'marked', 'bootstrap'], function($, formvalidate, marked, bootstrap){

	var msg_box = $(".login-msg");

	$("#userInput").on("blur", function(){
		var value = this.value;
		//illegal string
		if(!formvalidate.ValidateAccount(value))
		{
			msg_box.text("Invalid User Name");
		}
		else
		{
			msg_box.text("");
		}
	});

	$("#passwordInput").on("blur", function(){
		var value = this.value;
		if(!formvalidate.ValidatePassword(value))
		{
			msg_box.text("Invalid Password (At least 6-12 characters)");
		}
		else
		{
			msg_box.text("");
		}
	});

	$("#feature-btn").on('click', function(){
		var text = $("#textarea").val();
		$("#preview").html(marked(text));
	});

})
