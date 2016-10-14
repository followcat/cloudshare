require.config({
  baseUrl: "/static/",
  paths: {
    jquery: "lib/js/jquery",
    bootstrap: "lib/js/bootstrap",
    datetimepicker: "lib/js/bootstrap-datetimepicker.min",
    header: "src/js/util/header",
    formvalidate: "src/js/util/formvalidate",
    cvdeal: "src/js/util/cv_deal",
    Upload: "src/js/util/upload",
    colorgrad: "src/js/util/colorgrad",
    History: "src/js/util/history"
  },
  shim: {
    bootstrap: {
      deps: ["jquery"],
      exports: "bootstrap"
    },
    datetimepicker: {
      deps: ["jquery"],
      exports: "bootstrap-datetimepicker"
    },
    cvdeal: {
      deps: ["jquery"],
      exports: "cvdeal"
    }
  }
});

require([
  "jquery",
  "cvdeal",
  "datetimepicker",
  "Upload",
  "colorgrad",
  "History",
  "header",
  "bootstrap",
],function($, cvdeal, datetimepicker, Upload, ColorGrad, History) {

  cvdeal.cvDeal("cvContent", function() {
    $("#loading").css("display", "none");
  });

  var c = {
    currentUser: $("#name").text().trim(),

    project: localStorage.getItem('_pj'),

    id: function() {
      var url = String(window.location.href);
      var arr = url.split("/");
      return arr[arr.length - 1];
    }(),

    checkBlank: function(value) {
      var reg = /^\s*$/g;
      if (value === "" || reg.test(value)) {
        return true;
      } else {
        return false;
      }
    }
  };

  $("#formDatetime").datetimepicker({
    format: "yyyy-mm-dd",
    weekStart: 1,
    todayBtn: true,
    autoclose: true,
    todayHighlight: 1,
    startView: 2,
    minView: 2,
    pickerPosition: "bottom-left"
  });

  $("#trackingInput").on("focus", function() {
    $(this).next().show();
  });

  $("#commentInput").on("focus", function() {
    $(this).next().show();
  });

  $(".fold").on("click", function() {
    $(this).parent().hide();
  });

  //简历标签点击事件
  $("#addTag").on("click", function() {
    var _this = $(this);
    var tagText = _this.text().trim();

    if (tagText === "Add a Tag") {
      _this.text("Fold");
      $(_this.next()).css("display", "block");
    } else {
      _this.text("Add a Tag");
      $(_this.next()).css("display", "none");
    }
  });

  //提交简历新的标签
  $("#tagBtn").on("click", function() {
    var tagText = $("#tagText").val();

    if (c.checkBlank(tagText)) {
      $("#tagText").focus();
    } else {
      $.ajax({
        type: "PUT",
        url: "/api/cv/updateinfo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
          "id": c.id,
          "project": c.project,
          "update_info": {
            "tag": tagText
          }
        }),
        success: function(response) {
          if (response.code === 200) {
            $("#tagContainer").prepend("<span class='label label-primary' title='"+ c.currentUser +"'>"+ tagText +"</span>");
            $("#tagText").val("");
          } else {
            alert(response.message);
          }
        }
      });
    }
  });

  //Add tracking massage
  $("#trackingBtn").on("click", function() {
    var trackingText = $("#trackingInput").val().trim(),
        date = $("#formDatetime").val();

    if (c.checkBlank(trackingText) || date === "") {
      $("#trackingInput").focus();
    } else {
      $.ajax({
        type: "PUT",
        url: "/api/cv/updateinfo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
          "id": c.id,
          "project": c.project,
          "update_info": {
            "tracking": {
              "date": date,
              "text": trackingText
            }
          }
        }),
        success: function(response) {
          if (response.code === 200) {
            $("#trackingContent").prepend("<div class='tracking-item'><em>"+ c.currentUser +" / "+ date +"</em><p>"+ trackingText +"</p></div>");
            $("#trackingInput").val("");
          } else {
            alert(response.message);
          }
        }
      });
    }
  });

  //Add comment
  $("#commentBtn").on("click", function() {
    var commentText = $("#commentInput").val().trim();

    if (c.checkBlank(commentText)) {
      $("#commentInput").focus();
    } else {
      $.ajax({
        type: "PUT",
        url: "/api/cv/updateinfo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
          "id": c.id,
          "project": c.project,
          "update_info": {
            "comment": commentText
          }
        }),
        success: function(response) {
          if (response.code === 200) {
            $("#commentContent").prepend("<div class='comment-item'><em>"+ c.currentUser + " / " + response.data.date +"</em><p>" + response.data.content + "</p></div>");
            $("#commentInput").val("");
          } else {
            alert(response.message);
          }
        }
      });
    }
  });

  //Add url into the link button
  function Route() {
    $("#download").attr("href", "/download/" + c.id + ".doc");
    $("#modify").attr("href", "/modify/" + c.id + ".md");
    // $("#match").attr("href", "/resumetojd/" + c.filename + "/Opening");
  }
  Route();

  //upload english file
  $("#enUploadSubmit").on("click", function() {
    localStorage.name = c.id;

    var uploader = new Upload("enUploadForm");
    uploader.Uploadfile(function() {
      setTimeout(function() {
        window.location.href = "/preview";
      }, 1000);
    });
  });

  $(".upload-en-modal").on("click", function() {
    $("#enFile").val("");
    $("#enUploadMsg").html("");
  });

  localStorage.title = $("title").text().split("-")[0];


  //CV Title Data Modify

  //Tranform Title Data Modify status
  $("#modifyTitle").click(function() {
    if ($(this).attr("checked")) {
      $(this).removeAttr("checked");
      $("#cvTitleWrap").css("display", "none");
    } else {
      $(this).attr("checked", "checked");
      $("#cvTitleWrap").css("display", "block");
    }
  });


  //Title Button Handle
  $("#titleBtn").on("click", function() {
    $.ajax({
      url: "/api/cv/updateinfo",
      type: "PUT",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        "id": c.id,
        "project": c.project,
        "update_info": {
          "id": $("#titleId").val().trim(),
          "name": $("#titleName").val().trim(),
          "origin": $("#titleOrigin").val().trim(),
        }
      }),
      success: function(response) {
        if (response.code === 200) {
          window.location.reload();
        } else {
          alert(response.message);
        }
      }
    });
  });

  //Get similar person data.
  $.ajax({
    url: "/api/mining/similar",
    type: "post",
    dataType: "json",
    contentType: "application/json",
    data: JSON.stringify({
      "doc": $("#cvContent").text(),
      "project": localStorage.getItem('_pj')
    }),
    success: function(response) {
      var datas = response.data;
      for (var i = 0, len = datas.length; i < len; i++) {
        var _index = datas[i];
        var name = _index.yaml_info.name !== "" ? _index.yaml_info.name : _index.yaml_info.id;

        $("#similarContent").append("<div class='similar-item'><a href='/show/" + _index.id + "' target='_blank'>" +
          name + " | " + _index.yaml_info.position + " | " +
          _index.yaml_info.age + " | " + _index.yaml_info.gender + " | " + _index.yaml_info.education + "</a></div>"
        );
      }
    }
  });

  //Write history
  var history = new History();
  history.writeHistory({
    name: $("#titleName").val(),
    filename: c.id + ".md",
    id: $("#titleId").val(),
  });

  var topHeight = $("header").innerHeight() + parseInt($(".wrapper").css("marginTop"));
  $(document).scroll(function() {
    var top = $(document).scrollTop();
    if ( top > topHeight ) {
      $(".side").css({
        position: "fixed",
        top: "10px"
      });
    } else {
      $(".side").css({
        position: "absolute",
        top: "0"
      });
    }
  });

  //收藏简历请求
  $("#collect").on("click", function() {
    var _this = $(this),
        cvId = c.id,
        collected = _this.attr("data-collected");

    if (collected === "true") {
      $.ajax({
        url: "/delbookmark",
        type: "POST",
        data: {
          "id": cvId
        },
        success: function(response) {
          if (response.result) {
            _this.attr("data-collected", "false");
            _this.removeClass("star-active");
          } else {
            alert("Delete bookmark error.");
          }
        }
      });
    } else {
      $.ajax({
        url: "/addbookmark",
        type: "POST",
        data: {
          "id": cvId
        },
        success: function(response) {
          if (response.result) {
            _this.attr("data-collected", "true");
            _this.addClass("star-active");
          } else {
            alert("Add bookmark error.");
          }
        }
      });
    }
  });
});
