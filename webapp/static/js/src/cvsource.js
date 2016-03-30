require.config({
	baseUrl: '../static/js',
	paths: {
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		datetimepicker: 'lib/bootstrap-datetimepicker.min',
		datetimepickerCN: 'lib/bootstrap-datetimepicker.zh-CN',
		cvdeal: 'src/cvdeal',
		Upload: 'src/upload',
		colorgrad: 'src/color/colorgrad'
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


require(['jquery', 'bootstrap', 'datetimepicker', 'datetimepickerCN', 'cvdeal', 'Upload', 'colorgrad'], function($, bootstrap, datetimepicker, datetimepickerCN, cvdeal, Upload, ColorGrad) {

	window.onload = cvdeal.CVdeal();

	$('.form_date').datetimepicker({
		language: 'zh-CN',
		weekStart: 1,
		todayBtn: 1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		minView: 2,
		forceParse: 0
	});

	$("#tracking-text").on('focus', function() {
		$(this).next().show();
	});

	$("#comment-text").on('focus', function() {
		$(this).next().show();
	});

	$(".collapse").on('click', function() {
		$(this).parent().hide();
	});

	//add label function
	$("#add-label").on('click', function() {
		var display = $(".add-label-box").css("display");

		if (display === 'none') {
			$(this).text("收起");
			$(".add-label-box").css("display", "table");
		} else {
			$(this).text("添加标签");
			$(".add-label-box").css("display", "none");
		}

	});

	function GetFileName() {
		var url = String(window.location.href);
		var arr = url.split("/");
		var filename = arr[arr.length - 1];

		return filename;
	};

	function CheckBlank(val) {
		var reg = /^\s*$/g;
		if (val == "" || reg.test(val)) {
			return true;
		} else {
			return false;
		}

	}

	//Add tag
	$("#add-label-btn").on('click', function() {
		var filename = GetFileName();
		var label_text = $("#label-text").val();
		var current_user = $("#current-id").text();

		if (CheckBlank(label_text)) {
			$(this).attr("disable", false);
			$("#label-text").focus();
		} else {
			$(this).attr("disable", true);
			$.ajax({
				type: 'POST',
				url: '/updateinfo',
				dataType: 'json',
				contentType: 'application/json',
				data: JSON.stringify({
					"filename": filename,
					"yamlinfo": {
						"tag": label_text
					}
				}),
				success: function(result) {
					if (result.result) {
						$(".label-item").prepend("<span class='label label-primary' title=" + current_user + ">" + label_text + "</span>");
						$("#label-text").val("");
					} else {
						alert("操作失败");
					}
				}
			});
		}

	});

	//Add tracking massage 
	$("#tracking-btn").on('click', function() {
		var filename = GetFileName();
		var tracking_text = $("#tracking-text").val();
		var date = $("#date").val();
		var current_user = $("#current-id").text();

		if (CheckBlank(tracking_text) || date == "") {
			$(this).attr("disable", false);
			$("#tracking-text").focus();
		} else {
			$(this).attr("disable", true);
			$.ajax({
				type: 'POST',
				url: '/updateinfo',
				dataType: 'json',
				contentType: 'application/json',
				data: JSON.stringify({
					"filename": filename,
					"yamlinfo": {
						"tracking": {
							"date": date,
							"text": tracking_text
						}
					}
				}),
				success: function(result) {
					if (result.result) {
						$("#tracking-content").prepend("<div class='tracking-item'><p class='content'>" + tracking_text + "</p><em class='commit-info'>" + current_user + " " + date + "</em></div>");
						$("#tracking-text").val("");
					}
				}
			});
		}

	});

	//Add comment
	$("#comment-btn").on('click', function() {
		var filename = GetFileName();
		var comment_text = $("#comment-text").val();
		var current_user = $("#current-id").text();

		if (CheckBlank(comment_text)) {
			$(this).attr("disable", false);
			$("#comment-text").focus();
		} else {
			$(this).attr("disable", true);
			$.ajax({
				type: 'POST',
				url: '/updateinfo',
				dataType: 'json',
				contentType: 'application/json',
				data: JSON.stringify({
					"filename": filename,
					"yamlinfo": {
						"comment": comment_text
					}
				}),
				success: function(result) {
					$("#comment-content").prepend("<div class='comment-item'><em class='commit-info'>" + current_user + "</em><p class='content'>" + comment_text + "</p></div>");
					$("#comment-text").val("");
				}
			});
		}

	});

	var url = window.location.href.split('/');
	var filename = url[url.length - 1];

	function Route() {
		$("#download").attr('href', '/download/' + filename.split('.')[0] + '.doc');
		$("#modify").attr('href', '/modify/' + filename);
	}
	Route();

	//upload english file
	$("#upload-btn").on('click', function() {
		localStorage.name = filename;

		var uploader = new Upload("file-form");
		uploader.Uploadfile(function() {
			setTimeout(function() {
				window.location.href = "/preview";
			}, 1000);
		});
	});
	$(".upload").on('click', function() {
		$("#file").val("");
		$("#progressmsg").html("");
	});

	localStorage.title = $('title').text().split('-')[0];


	//CV Title Data Modify

	//Tranform Title Data Modify status
	$('#tranform-check').click(function() {
		if ($(this).attr('checked')) {
			$(this).removeAttr('checked');
			$('#title-table tbody tr input').attr('disabled', 'disabled');
			$('#title-submit-btn').css('display', 'none');
		} else {
			$(this).attr('checked', 'checked');
			$('#title-table tbody tr input').removeAttr('disabled');
			$('#title-submit-btn').css('display', 'block');
		}
	});


	//Title Button Handle
	$('#title-submit-btn').on('click', function() {
		var filename = window.location.href.split('/');
		filename = filename[filename.length - 1];

		$.ajax({
			url: '/updateinfo',
			type: 'post',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify({
				'filename': filename,
				'yamlinfo': {
					'id': $('#Id').val(),
					'name': $('#name').val(),
					'origin': $('#origin').val()
				}
			}),
			success: function(response) {
				if (response.result) {
					window.location.reload();
				} else {
					alert('提交失败');
				}
			}
		});
	});

	$.ajax({
		url: '/analysis/lsi',
		type: 'post',
		data: {
			'doc': document.getElementById("cv-content").innerText
		},
		success: function(response) {
			var datas = response.result,
				colorgrad = ColorGrad();
			for(var i = 0, len = datas.length; i < len; i++){
				var fileName = datas[i][0],
					name = datas[i][1].name,
					match = datas[i][2].match;

				colorStyle = colorgrad.gradient(parseInt(match*100));
				$('#similar-person').append("<a href=\"/show/"+ fileName +"\" style=\"color:"+ colorStyle +"\" target=\"_blank\">" + name + "</a>");
			}
		}
	});
});