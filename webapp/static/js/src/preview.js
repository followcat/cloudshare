require.config({
	baseUrl: '../static/js',

	paths: {
		jquery: 'lib/jquery',
		cvdeal: 'src/cvdeal',
		bootstrap: 'lib/bootstrap'
	},
	shim: {
		cvdeal:{
			deps: ['jquery'],
			exports: 'cvdeal'
		},
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		}
	}
});

require(['jquery', 'cvdeal', 'bootstrap'], function($, cvdeal, bootstrap){

	//load the origin data to the origin dropdown menu
	var LoadOrigin = function(){
		$.getJSON('/static/origindata.json', function(data){
			var menu = $("#origin-menu");
			$.each(data, function(index, value){
				if(index === 0)
				{
					$(".origin").text(value['origin']);
				}
				menu.append("<li><a href='javascript:;'>" + value['origin'] + "</a></li>");
			});
		});
	};

	//document were load ready, load the function
	$(document).ready(function(){
		cvdeal.CVdeal();
		LoadOrigin();
	});

	$("#origin-menu").delegate('a', 'click', function(){
		var value = $(this).text();
		$(".origin").text(value);
	});

	$("#confirm-btn").on('click', function(){
		var aForm = $("#cv-confirm-form");
		var aText = aForm.find(":text");


		if(aText[0].value !== "" && aText[1].value !== "" && aText[2].value !== "")
		{
			$.ajax({
				url: '/confirm',
				type: 'POST',
				data: aForm.serialize(),
				success: function(result){
					if(result.result)
					{
						setTimeout(function(){
							window.location.href = "/search";
						},500);
					}
					else
					{
						alert('文件已存在或者该简历不存在联系方式');
					}
				}
			});
		}	
        
	});

	//go back history
	$("#goback-btn").on('click', function(){
		history.go(-1);
	})

});