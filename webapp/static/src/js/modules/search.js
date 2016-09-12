require.config({
  baseUrl: "/static/",
  paths: {
    jquery: 'lib/js/jquery',
    bootstrap: 'lib/js/bootstrap',
    header: 'src/js/util/header',
    formvalidate: 'src/js/util/formvalidate',
    Upload: 'src/js/util/upload',
    History: 'src/js/util/history'
  },
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    }
  }
});

require(['jquery', 'bootstrap', 'header', 'formvalidate', 'Upload', 'History'], function($, bootstrap, header, formvalidate, Upload, History){

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

  //User info page - read history
  var history = new History();
  var lists = history.readHistory() ? history.readHistory() : [];

  if ( typeof lists === 'undefined' ) {
    $('#browing-wrap').append('<p>You have no browsing history.</p>');
  } else {
    lists.reverse();
    for (i = 0, len = lists.length; i < len; i++) {
      if( i === 10 ) {
        break;
      }
      $('#browing-wrap').append("<div class='list-item'><span>"+ lists[i].time +"</span><a href='/show/"+ lists[i].filename +"'>"+ lists[i].name +"</a></div>");
    }
  }

  function formDisplay() {
    if( $("#check").is(":checked") ) {
      $("#serachbykey").css("display", "none");
      $("#serachbysentence").css("display", "block");
    }else {
      $("#serachbykey").css("display", "block");
      $("#serachbysentence").css("display", "none");
    }
  }
  formDisplay();
  $(".type-check label").on("click", function(){
    if( !$("#check").is(":checked") ) {
      $("#serachbykey").css("display", "none");
      $("#serachbysentence").css("display", "block");
    }else {
      $("#serachbykey").css("display", "block");
      $("#serachbysentence").css("display", "none");
    }
  });

  var databaseList = localStorage.databaseList ? JSON.parse(localStorage.databaseList) : [];

  if (databaseList.length > 0) {
    $("#serachbysentence").append("<input type=\"text\" class=\"hide-param\" name=\"uses\" value=\""+ databaseList.join(",") +"\" />");
  }

  $.ajax({
    url: "/cvnumbers",
    dataType: "json",
    success: function(response) {
      var numbers = response.result,
          len = 0;
      for (var e in numbers) {
        len++;
      }
      var mgLeft = (720 - len * 80) / (len + 1);

      for (var e in numbers) {
        $("#count").append("<div class=\"count-item\" style=\"margin-left: " + mgLeft+"px"+ "\">" + 
          "<div class=\"k\">" + e +
          "</div>" +
          "<div class=\"n\">" + numbers[e] +
          "</div>" +
          "</div>"
        );
      }
    }
  });

  //删除收藏
  $(".delete").on("click", function() {
    var _this = $(this),
        collectionLinkObj = _this.prev();
    var id = collectionLinkObj.attr("data-id");
    $.ajax({
      url: "/delbookmark",
      type: "POST",
      data: {
        "id": id
      },
      success: function(response) {
        if (response.result) {
          _this.parent().remove();
        } else {
          alert("Delete error.")
        }
      }
    });
  });
});
