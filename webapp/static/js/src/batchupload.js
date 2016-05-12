(function(){

	function checkFileObj(fileName){

		var fileObjs = $('.ajax-file-upload-filename');

			for(var i = 0, len = fileObjs.length; i < len; i++){

				if( $(fileObjs[i]).text().indexOf(fileName) !== -1 ){

					return fileObjs[i];

				}

		}

		return 0;

	}

  var fileNameListObj = {};

	var uploadObj = $("#fileuploader").uploadFile({

		url:"/batchupload",

		fileName:"files",

		sequential:true,

		sequentialCount:1,

		autoSubmit:false,

		onLoad:function(obj)
		{
				$("#message").html($("#message").html()+"<p>上传控件已加载:</p>");
		},

		onSubmit:function(files)
		{

			$("#message").html($("#message").html()+"<p>提交:"+JSON.stringify(files)+"中...</p>");
			//return false;
		},

		onSuccess: function(files,data,xhr,pd){

			if(data.result){

				$("#message").html($("#message").html()+"<p style='color:green;'>提交:"+JSON.stringify(files) + "成功</p>");

			}else{

				$("#message").html($("#message").html()+"<p style='color:red;'>提交:"+JSON.stringify(files) + "失败,文件已存在</p>");

			}

			var thisElement = checkFileObj(files[0]);

			$(thisElement).parent().append('<div class=\'form-inline\'>' + 
				'<div class=\'form-group\'>' +
				'<label>Name<\/label>' +
				'<input class=\'form-control input-sm name\' value=\''+ data.name +'\'>' +
				'<\/div><\/div>');

			fileNameListObj[files[0]] = null;

		},

		onError: function(files,status,errMsg,pd){

			$("#message").html($("#message").html()+"<p style='color:red;'>提交:"+JSON.stringify(files) + "错误.(" + status + ":" + errMsg + ")</p>");

		},

		afterUploadAll:function(obj){

			$("#message").html($("#message").html()+"<p/>所有文件分析已经完成！</p>");

			$('#message').prepend('<p style=\'color:red;\'>请点击确认按钮确认所有上传文件！<\/p>');

		},
	});

	$('#start-upload').on('click', function(){

		uploadObj.startUpload();

	});

	$('#confirm-btn').on('click', function(){

    var allName = true;

    $.each(fileNameListObj, function(index, data){

    	var element = checkFileObj(index);

    	if(element){

    		var nameInput = $(element).parent().find('.name');

    		if($(nameInput).val() !== ''){

    			var obj = {};

    			obj.name = $(nameInput).val();

    			fileNameListObj[index] = obj;

    			obj = null;

    			allName = true;

    		}else{

    			$(nameInput).focus();

    			allName = false;

    			return false;

    		}

    	}

    });


    if( allName){

    	$.ajax({

				url: '/batchconfirm',

				type: 'post',

				data: {

					'updates': JSON.stringify(fileNameListObj)

				},
				success: function(response){

					$('#message').html('');

					$.each(response.result, function(index, data){

						if(data){

							$('#message').append('<p style=\'color:green\'>上传<strong>'+ index +'</strong>成功！</p>');

						}else{

							$('#message').append('<p style=\'color:red\'>上传<strong>'+ index +'</strong>失败！文件或已经存在.</p>');

						}

					});

				}

			});

    }

	});

}());
