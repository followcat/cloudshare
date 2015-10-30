window.onload = function(){
	$("#cv-confirm").on('click', function(){

	    if(confirm("Are you sure to submit?"))
	    {
	        $.get('/confirm',function(result){
	            if(result == 'True')
	            {
	                window.location.href = '/search';
	            }
	            else
	            {
	                alert(' Exists File ');
	            }
	        });
	    }  
	});

	
	var cvdeal = {};

	// delete hr  Function
	cvdeal.DeleteHr = function(){
		$("hr").remove();
	};

	//delete id named "section *"  Function
	cvdeal.DeleteSection = function(){
		var reg = /section-\d+|section/;
		var aH2 = $("h2");

		aH2.each(function(){
			if(reg.test(this.id))
			{
				this.remove();
			}
		});
	};

	//delete link of chinese  Function
	cvdeal.DeleteLink = function(){
		var reg = /[\u4e00-\u9fa5]+/;

		//get body children p
		var childP = $("body").children("p");

		childP.each(function(){
			var a = $(this).children("a");
			var a_text = a.text();
			if(reg.test(a_text) && a_text !== "")
			{
				a.remove();
			}
		});

	};


	//delete --------- breaket  Function
	cvdeal.DeleleLine = function(){
		var pattern = /-{3,}/g;
		var patternTd = /-{2,}/g;

		var patternPbr = /\d(\.|：|:|、).*(；|;|\.|。)/g;

		var allElementP = $("p");
		var allElementTh = $("th");
		var allElementTd = $("td");

		allElementP.each(function(){

			var text = $(this).text();

			if(pattern.test(text))
			{
				text = text.replace(pattern," ");
				$(this).text(text);
			}
			if(patternPbr.exec(text))
			{
				
			}
		});

		allElementTh.each(function(){
			var text = $(this).text();
			if(pattern.test(text))
			{
				$(this).parent().remove();
			}
		});

		allElementTd.each(function(){
			
			var text = $(this).text();

			if(pattern.test(text))
			{
				var retext = text.replace(pattern," ");
				$(this).text(retext);
			}


			// if(text !== "" && $(this).next("td").text() === "")
			// {
			// 	console.log($(this).next());
			// 	$(this).attr("colspan","1");
			// 	cvdeal.CheckBlank($(this));
			// }
		});
	};

	// cvdeal.CheckBlank = function(obj){
	// 	var nextBro = obj.next();
	// 	if(nextBro.text() === "")
	// 	{
	// 		nextBro.remove();
	// 		var colspan = parseInt(obj.attr("colspan"));
	// 		colspan++;
	// 		obj.attr("colspan",colspan);
	// 	}
		
	// }

	// delete hr
	cvdeal.DeleteHr();
	//delete id named "section *"
	cvdeal.DeleteSection();
	//delete link of chinese
	cvdeal.DeleteLink();

	cvdeal.DeleleLine();
};