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

  $("#sentenceBtn").on("click", function() {
    var sbs = $("#serachbysentence"),
        databaseList = localStorage.databaseList ? JSON.parse(localStorage.databaseList) : [];

    if (databaseList.length > 0) {
      var usesInput = sbs.find("input[name='uses']");
      if (usesInput.length > 0) {
        $(usesInput).val(databaseList.join(","));
      } else {
        $(sbs).append("<input type=\"text\" class=\"hide-param\" name=\"uses\" value=\""+ databaseList.join(",") +"\" />");
      }
    }

    if (localStorage.model) {
      var modelInput = sbs.find("input[name='model']");
      if (modelInput.length > 0) {
        $(modelInput).val(localStorage.model);
      } else {
        $(sbs).append("<input type=\"text\" class=\"hide-param\" name=\"model\" value=\""+ localStorage.model +"\" />");
      }
    }
    $(sbs).submit();
  });

  function objectToArray(obj) {
    var arr = [];
    for (var e in obj) {
      arr.push({ name: e, number: obj[e] });
    }

    return arr;
  }

  function compare(obj1, obj2) {
    if (obj1.number < obj2.number) {
      return 1;
    } else if (obj1.number > obj2.number) {
      return -1;
    } else {
      return 0;
    }
  }
  $.ajax({
    url: "/cvnumbers",
    dataType: "json",
    success: function(response) {
      var data = response.result;
      var classifyDatas = objectToArray(data);
      classifyDatas.sort(compare);

      for (var i = 0, len = classifyDatas.length; i < len; i++) {
        if (classifyDatas[i].name === "total") {
          $("#total").append(classifyDatas[i].name.toUpperCase() + ": " + classifyDatas[i].number);
        } else if (classifyDatas[i].name === "cloudshare") {
          $("#countList").prepend("<div class=\"count-list-item\">" + classifyDatas[i].name.toUpperCase() + ": " + classifyDatas[i].number + "</div>");
        } else if (classifyDatas[i].number !== 0){
          $("#countList").append("<div class=\"count-list-item\">" + classifyDatas[i].name.toUpperCase() + ": " + classifyDatas[i].number + "</div>");
        }
      }
    }
  });

  $("#total").on("click", function() {
    if ($("#countList").css("display") === "none") {
      $("#countList").css("display", "block");
    } else {
      $("#countList").css("display", "none");
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
