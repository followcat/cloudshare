require.config({
  baseUrl: "../static/js",
  paths: {
    jquery: 'lib/jquery',
    bootstrap: 'lib/bootstrap',
    header: 'src/header',
    formvalidate: 'src/formvalidate',
    Upload: 'src/upload',
    Cookies: 'src/cookies'
  },
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    }
  }
});

require(['jquery', 'bootstrap', 'header', 'formvalidate', 'Upload', 'Cookies'], function($, bootstrap, header, formvalidate, Upload, Cookies){
  var item = $('.operate-list-item');

  for(var i = 0, len = item.length; i < len; i++){
    var strFile = $(item[i]).find('.filename').text(),
        strName = $(item[i]).find('.name').text(),
        strMsg = $(item[i]).find('p').text();
    var link = '';
    if(strName === ''){
      link = "<a href='/show/" + strFile + ".md' target='_blank'>" + strFile + "</a>";
    }else{
      link = "<a href='/show/" + strFile + ".md' target='_blank'>" + strName + "</a>";
    }
    strMsg = strMsg.replace(strFile, link);
    $(item[i]).find('p').html(strMsg);
  }

  //User info page - read cookies
  var cookie = new Cookies();
  var lists = cookie.readCookie();

  if ( typeof lists === 'undefined' ) {
    $('#browing-wrap').append('<p>You have no browsing history.</p>');
  } else {
    lists.reverse();
    for (i = 0, len = lists.length; i < len; i++) {
      if( i === 10 ) {
        break;
      }
      $('#browing-wrap').append("<div class='list-item'><span>"+ lists[i].time +"</span><a href='/show/"+ lists[i].fileName +"'>"+ lists[i].name +"</a></div>");
    }
  }

  $("#search").on("click", function(){
    $("#search-form").attr("action", "/search").submit();
  });

  $("#check").on("click", function(){
    $("#search-form").attr({
      action: "/analysis/lsi",
      method: "post"
    }).submit();
  });
});
