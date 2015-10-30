require.config({
	baseUrl: "../static/js",

	paths: {
		jquery: 'lib/jquery',
		formvalidate: 'src/formvalidate',
		marked: 'lib/marked'
	},

	shim: {
		marked: {
			exports: 'marked'
		}
	}
})

require(['jquery', 'formvalidate', 'marked'], function($, formvalidate, marked){

	var msg_box = $(".login-msg");

	$("#userInput").on("blur", function(){
		var value = this.value;
		//illegal string
		if(!formvalidate.ValidateAccount(value))
		{
			msg_box.text("illegal account");
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
			msg_box.text("illegal password. At least 6-12 strings");
		}
		else
		{
			msg_box.text("");
		}
	});

	$("#textarea-input").on('change', function(){
		$("#preview").html(marked(this.value));
	})
})