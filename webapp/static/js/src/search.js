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

  var item = $('.operate-list-item');

  for(var i = 0, len = item.length; i < len; i++){

		  var strFile = $(item[i]).find('.filename').text();

		  var strName = $(item[i]).find('.name').text();

		  var strMsg = $(item[i]).find('p').text();

    var link = '';

    if(strName === ''){
      link = "<a href='/show/" + strFile + ".md' target='_blank'>" + strFile + "</a>";
    }else{
      link = "<a href='/show/" + strFile + ".md' target='_blank'>" + strName + "</a>";
    }

		  strMsg = strMsg.replace(strFile, link);

    $(item[i]).find('p').html(strMsg);

  }
});