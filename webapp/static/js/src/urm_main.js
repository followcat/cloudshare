define(['jquery'], function(){
	var urmmain = {};

	//Left wrap navigation click function
	urmmain.NavLinkClass = function(){
		var aLink = $("#nav-list li a");

		//judge it is current link and add class
		aLink.each(function(){
			if($(this)[0].href == String(window.location)){
				$(this).addClass("active");		
			}
			
		})

		aLink.on('click', function(){
			
			$("#nav-list li a").removeClass();
			$(this).addClass("active");
		})
	}
	urmmain.NavLinkClass();

	urmmain.Quit = function(){
		var quitBtn = $("#quit-btn");
		quitBtn.on('click', function(event){
			
			$.ajax({
				url: '/logout',
				type: 'GET',
				success: function(){
					window.location.href = "/";
				},
				error: function(msg){
					alert("Operate Error!");
					console.log(msg);
				}

			})

			event.preventDefault();
		})

	}
	urmmain.Quit();

	//form ajax submit function
	urmmain.FormAjax = function(formObj,success_func,fail_func){

		$.ajax({
			url: formObj.attr('action'),
			type: formObj.attr('method'),
			dataType: 'text',
			data: formObj.serialize(),
			success: function(result){
				var resultJson = $.parseJSON(result);
				if(resultJson.result)
				{
					success_func();
				}
				else
				{
					fail_func();
				}
			},
			error: function(msg){
				console.log(msg);
				alert("Error!")
			}
		});


	}

	//set up the button of save to open or close
	urmmain.ButtonDisable = function(obj){
		obj.attr("disabled",true);
	}

	urmmain.ButtonAble = function(obj){
		obj.attr("disabled",false);
	}

	return urmmain;
})