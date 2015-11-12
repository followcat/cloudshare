require.config({
	baseUrl: "../static/js",

	paths: {
		jquery: 'lib/jquery',
		bootstrap: 'lib/bootstrap',
		header: 'src/header',
		formvalidate: 'src/formvalidate',
		Upload: 'src/upload'
	},
	shim: {
		bootstrap: {
			deps: ['jquery'],
			exports: 'bootstrap'
		}
	}
});


require(['jquery', 'bootstrap', 'header', 'formvalidate', 'Upload'], function($, bootstrap, header, formvalidate, Upload){

	//deal with something information
	var infoDeal = {};

	//if name is null, add name...
	infoDeal.NameAdd = function(){
		$(".name").each(function(){
			var aName = $(this);
			var nameBox = aName.find("span");
			var name_text = nameBox.text();
			if(name_text === "")
			{
				var title = aName.parent().parent().prev().find("a").text();
				var name = title.split("-")[0];
				nameBox.text(name);
			}
		});
	};
	infoDeal.NameAdd();
	
	//if age is "[]", delete the string of "[]"...
	infoDeal.DeleteSqBK = function(){
		$(".age").each(function(){
			var aAge = $(this);
			var ageBox = aAge.find("span");
			var age_text = ageBox.text();
			if(age_text === "[]")
			{
				ageBox.text("");
			}

		});
	};
	infoDeal.DeleteSqBK();


	function Toggle(obj){
		obj.click(function(){
			var This = $(this);
			var aBlock = This.next();
			
			if(This.children().text() == "+"){
				This.children().text("-");
				aBlock.show();
				obj.flag = true;
			}else{
				This.children().text("+");
				aBlock.hide();
				This.flag = false;
			}

		});
	}
	var aLabelToggle = $(".label-alink");
	Toggle(aLabelToggle);

	var aCommentToggle = $(".comment-alink");
	Toggle(aCommentToggle);

	function AddedInfoHandler(obj){
		var nextBro = obj.next();
		if(nextBro.css("display") === "none"){
			obj.children("span").text("-");
			nextBro.show();
		}else{
			obj.children("span").text("+");
			nextBro.hide();
		}
	}

	//tracking-link click event
	$(".tracking-link").on('click', function(){
		AddedInfoHandler($(this));
	});

	//comment-link click event
	$(".comment-link").on('click', function(){
		AddedInfoHandler($(this));
	});
});