require.config({
	baseUrl: '../static/js',

	paths: {
		jquery: 'lib/jquery',
		cvdeal: 'src/cvdeal'
	},
	shim: {
		cvdeal:{
			deps: ['jquery'],
			exports: 'cvdeal'
		}
	}
});

require(['jquery', 'cvdeal'], function($, cvdeal){

	window.onload = cvdeal.CVdeal();
	$("#confirm-btn").on('click', function(){
		var aForm = $("#cv-confirm-form");
		var aText = aForm.find(":text");


		if(aText[0].value !== "" && aText[1].value !== "" && aText[2].value !== "")
		{
			$.ajax({
				url: '/confirm',
				type: 'POST',
				data: aForm.serialize(),
				dataType: 'text',
				success: function(result){
					if( result == 'True')
					{
						window.location.href = '/search';
					}
					else
					{
						alert('文件已存在或者该简历不存在联系方式');
					}
				}
			});
		}	
        
	});




});