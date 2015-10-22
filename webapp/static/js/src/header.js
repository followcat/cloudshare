define(['jquery'], function($){

	var header = {};

	//upload modal, button of choose file config
	header.UploadChooseFile = function(btnObj, fileTextObj){
		
		btnObj.on("change", function(){
			fileTextObj.val(this.value);
		})
	};

	// Login out in header
	header.LogOut = function(obj){
		//obj is a element object
		obj.on("click", function(event){
			$.ajax({
				url: '/logout',
				type: 'GET',
				success: function(){
					window.location.href = "/index";
				},
				error: function(msg){
					alert(msg);
				}
			})

			event.preventDefault();    //prevent event default.
		})

	}



	return header;
})