require.config({
	baseUrl: '../static/js',
	paths: {
		jquery: 'lib/jquery',
		cvdeal: 'src/cvdeal'
	},
	shim: {
		cvdeal: {
			deps: ['jquery'],
			exports: 'cvdeal'
		}
	}
});

require(['jquery', 'cvdeal'], function($, cvdeal){
	window.onload = cvdeal.CVdeal();

	function Edit(obj){
		obj.on('dblclick', function(){
			if(!$(this).children().is('textarea')){
				$(this).find('#delete').remove();
				var text = $(this).html();
				$(this).html("<textarea cols='24' wrap='hard'>" + text + "</textarea>");

				$(this).find('textarea').focus().on('blur', function(){
					var val = $(this).val();
					$(this).parent().html(val);
				});
			}
		});

		obj.on('mouseenter', function(){
			$(this).append("<button type='button' id='delete' class='close'><span aria-hidden='true'>&times;</span></button>");
			$(this).find("#delete").css({
				'position' : 'absolute',
				'right' : '0',
				'top' : '0'
			}).on('click', function(){
				$(this).parent().remove();
			});
		});

		obj.on('mouseleave', function(){
			$(this).find('#delete').remove();
		});
	}

	var oTd = $("td");
	var oP = $("p");
	Edit(oTd);
	Edit(oP);

	// 	// export html to file
	// function fake_click(obj) {
 //    var ev = document.createEvent("MouseEvents");
 //    ev.initMouseEvent(
 //        "click", true, false, window, 0, 0, 0, 0, 0
 //        , false, false, false, false, 0, null
 //        );
 //    obj.dispatchEvent(ev);
	// }
	 
	// function export_raw(name, data) {
	//    var urlObject = window.URL || window.webkitURL || window;
	 
	//    var export_blob = new Blob([data]);
	 
	//    var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a")
	//    save_link.href = urlObject.createObjectURL(export_blob);
	//    save_link.download = name;
	//    fake_click(save_link);
	// }
	var content = $('#cv-box').html();
	var obj = $(content);
	console.log(content);
	$('#exports-btn').click(function() {
		var content = $('#cv-content').html();
		var header = $("header").html();
		var style = $("style").html();
		var meta = "<meta charset='utf-8'>";
		var html = meta
		 					+ "<style>" + style + "</style>" 
							+ "<header class='header-box'>" + header + "</header>"
							+ "<div id='cv-box'><div id='cv-content'>"
							+ content
							+ "</div></div>";
		var filename = $('title').text();

		var link = document.createElement('a');
    mimeType = 'text/html';
    link.setAttribute('download', filename);
    link.setAttribute('href', 'data:' + mimeType  +  ';charset=utf-8,' + encodeURIComponent(html));
    link.click();
		// export_raw(filename + '.html', html);
	});

	function setTitle(){
		var title = localStorage.title;
		localStorage.removeItem('title');
		$('title').text(title);
	}
	setTitle();

	function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);


    var dataURL = canvas.toDataURL("image/png");

    return dataURL;
	}

	//logo image to base64
	$('.logo')[0].src = getBase64Image($('.logo')[0]);

});