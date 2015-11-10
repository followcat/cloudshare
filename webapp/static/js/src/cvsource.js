require.config({
	baseUrl: '../static/js',
	paths: {
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		datetimepicker: 'lib/bootstrap-datetimepicker.min',
		datetimepickerCN: 'lib/bootstrap-datetimepicker.zh-CN',
		cvdeal: 'src/cvdeal'
	},
	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		},
		datetimepicker: {
			deps: ['jquery'],
			exports: 'bootstrap-datetimepicker'
		},
		datetimepickerCN: {
			deps: ['jquery'],
			exports: 'bootstrap-datetimepicker-zh-CN'
		},
		cvdeal: {
			deps: ['jquery'],
			exports: 'cvdeal'
		}
	}
});


require(['jquery', 'bootstrap', 'datetimepicker', 'datetimepickerCN', 'cvdeal'], function($, bootstrap, datetimepicker, datetimepickerCN, cvdeal){
	
	window.onload = cvdeal.CVdeal();

	$('.form_date').datetimepicker({
    language:  'zh-CN',
    weekStart: 1,
    todayBtn:  1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    minView: 2,
    forceParse: 0
  });

	$("#tracking-text").on('focus', function(){
		$(this).next().show();
	});

	$("#comment-text").on('focus', function(){
		$(this).next().show();
	});

	//add label function
	$("#add-label").on('click', function(){
		var display = $(".add-label-box").css("display");

		if( display === 'none'){
			$(this).text("收起");
			$(".add-label-box").css("display", "table");
		}else{
			$(this).text("添加");
			$(".add-label-box").css("display", "none");
		}
		
	});

	function GetFileName(){
		var url = String(window.location.href);
		var arr = url.split("/");
		var filename = arr[arr.length-1];

		return filename;
	};

	//Add tag
	$("#add-label-btn").on('click', function(){
		var filename = GetFileName();
		var label_text = $("#label-text").val();

		$.ajax({
			type: 'POST',
			url: '/updateinfo',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				"filename" : filename,
				"yamlinfo" : {"tag" : label_text}
			}),
			success: function(result){
				console.log(result);
			},
			error: function(msg){
				console.log(msg);
			}
		});
	});

	//Add tracking massage 
	$("#tracking-btn").on('click', function(){
		var filename = GetFileName();
		var follow_up_text = $("#tracking-text").val();
		var date = $("#date").val();

		$.ajax({
			type: 'POST',
			url: '/updateinfo',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				"filename" : filename,
				"yamlinfo" : {
					"tracking" :{
						"date" : date,
						"text" : follow_up_text
					}
				}
			}),
			success: function(result){
				console.log(result);
			},
			error: function(msg){
				console.log(msg);
			}
		});
	});

	//Add comment
	$("#comment-btn").on('click', function(){
		var filename = GetFileName();
		var comment_text = $("#comment-text").val();

		$.ajax({
			type: 'POST',
			url: '/updateinfo',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				"filename" : filename,
				"yamlinfo" : { "comment" : comment_text }
			}),
			success: function(result){
				console.log(result);
			},
			error: function(msg){
				console.log(msg);
			}
		});
	});


});