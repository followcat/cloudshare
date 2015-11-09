define(['jquery'], function(){


	// $("#confirm-btn").on('click', function(){
	// 	var aForm = $("#cv-confirm-form");
	// 	var aText = aForm.find(":text");


	// 	if(aText[0].value !== "" && aText[1].value !== "" && aText[2].value !== "")
	// 	{
	// 		$.ajax({
	// 			url: '/confirm',
	// 			type: 'POST',
	// 			data: aForm.serialize(),
	// 			dataType: 'text',
	// 			success: function(result){
	// 				console.log(result);
	// 				if( result == 'True')
	// 				{
	// 					window.location.href = '/search';
	// 				}
	// 				else
	// 				{
	// 					alert('文件已存在或者该简历不存在联系方式');
	// 				}
	// 			}
	// 		});
	// 	}	
        
	// });

	//Object CVDeal
	function CVDeal(cv){
		this.cv = cv;
	}

	//Delete hr element
	CVDeal.prototype.DeleteHr = function(){
		var oHr = this.cv.find("hr");
		oHr.remove();
	};

	//Delete section element which text is a string likes "----"
	CVDeal.prototype.DeleteSection = function(){
		var reg = /section-\d+|section/;
		var aH2 = this.cv.find("h2");

		aH2.each(function(){
			if(reg.test(this.id))
			{
				this.remove();
			}
		});
	};

	//Delete pragraph's link
	CVDeal.prototype.DeleteLink = function(){
		var reg = /[\u4e00-\u9fa5]+/;

		var childP = this.cv.children("p");

		childP.each(function(){
			var a = $(this).children("a");
			var a_text = a.text();

			if( reg.test(a_text) && a_text !== "" )
			{
				a.remove();
			}
		});
	};


	CVDeal.prototype.DeleleLine = function(){
		var pattern = /-{3,}/g;

		var allElementP = this.cv.find("p");
		var allElementTh = this.cv.find("th");
		var allElementTd = this.cv.find("td");

		allElementTh.each(function(){
			var text = $(this).text();

			if(pattern.test(text))
			{
				$(this).parent().remove();
			}
		});

		allElementP.each(function(){
			var oP = $(this);
			var reg = /&nbsp;/;
			if(reg.test(oP.html()))
			{
				oP.remove();
			}

			CVDeal.prototype.ParagraphBr(oP, pattern);
		});

		allElementTd.each(function(){

			CVDeal.prototype.ParagraphBr($(this), pattern);
		});
	};

	CVDeal.prototype.ParagraphBr = function(obj, pattern){
		var text = obj.text();

		var patternChinese = /[\u4e00-\u9fa5]{15,}/;
		var patternPbr1 = /；|;/g;
		var patternPbr2 = /。/g;

		if(pattern.test(text))
		{
			text = text.replace(pattern,"");
			obj.text(text);
		}

		if(patternChinese.test(text))
		{
			text = text.replace(patternPbr1, "；<br />");
			text = text.replace(patternPbr2, "。<br />");
			obj.html(text);
		}
	};

	return {
		CVdeal: function(){
			var objCV = new CVDeal($("#cv-box"));

			objCV.DeleteHr();
			objCV.DeleteSection();
			objCV.DeleteLink();
		  objCV.DeleleLine();

		  objCV = null;

			$("#loding-img").remove();
			$("#cv-box").show();
		}
	};
});