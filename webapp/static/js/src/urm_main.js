define(['jquery'], function(){
	var urmmain = {};

	//Left wrap navigation click function
	urmmain.NavLinkClass = function(){

	}


	urmmain.FormAjax = function(formObj){

		$.ajax({
			url: formObj.attr('action'),
			type: formObj.attr('method'),
			dataType: 'html',
			data: formObj.serialize(),
			success: function(result){
				console.log('!!!')
			}

		})
	}
	return urmmain;
})