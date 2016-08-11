require.config({
  baseUrl: "/static/",
  paths: {
    jquery: "lib/js/jquery",
    bootstrap: "lib/js/bootstrap",
    datetimepicker: "lib/js/bootstrap-datetimepicker.min",
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
    datetimepickerCN: {
      deps: ["jquery"],
      exports: "bootstrap-datetimepicker-zh-CN"
    },
    cvdeal: {
      deps: ["jquery"],
      exports: "cvdeal"
    }
  }
});

require([
  "jquery",
  "bootstrap",
  "datetimepicker",
  "cvdeal",
  "Upload",
  "colorgrad",
  "History"
],function($, bootstrap, datetimepicker, cvdeal, Upload, ColorGrad, History) {

  cvdeal.cvDeal("cvContent", function() {
    $("#loading").css("display", "none");
  });

  var c = {
    currentUser: $("#name").text().trim(),

    filename: function() {
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
        type: "POST",
        url: "/updateinfo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
          "filename": c.filename,
          "yamlinfo": {
            "tag": tagText
          }
        }),
        success: function(response) {
          if (response.result) {
            $("#tagContainer").prepend("<span class='label label-primary' title='"+ c.currentUser +"'>"+ tagText +"</span>");
            $("#tagText").val("");
          } else {
            alert("Add tag failed");
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
        type: "POST",
        url: "/updateinfo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
          "filename": c.filename,
          "yamlinfo": {
            "tracking": {
              "date": date,
              "text": trackingText
            }
          }
        }),
        success: function(result) {
          if (result.result) {
            $("#trackingContent").prepend("<div class='tracking-item'><em>"+ c.currentUser +" / "+ date +"</em><p>"+ trackingText +"</p></div>");
            $("#trackingInput").val("");
          } else {
            alert("Failed");
          }
        }
      });
    }
  });

  //Add comment
  $("#commentBtn").on("click", function() {
    var commentText = $("#commentInput").val().trim(),
        dateNow = new Date();
    
    var y = dateNow.getFullYear(),
        mon = dateNow.getMonth() + 1,
        d = dateNow.getDate(),
        h = dateNow.getHours(),
        m = dateNow.getMinutes(),
        s = dateNow.getSeconds();

    var date = y+"-"+mon+"-"+d+" "+h+":"+m+":"+s;

    if (c.checkBlank(commentText)) {
      $("#commentInput").focus();
    } else {
      $.ajax({
        type: "POST",
        url: "/updateinfo",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
          "filename": c.filename,
          "yamlinfo": {
            "comment": {
              "date": date,
              "text": commentText,
            }
          }
        }),
        success: function(response) {
          if (response.result) {
            $("#commentContent").prepend("<div class='comment-item'><em>"+ c.currentUser + " / " + date +"</em><p>" + commentText + "</p></div>");
            $("#commentInput").val("");
          } else {
            alert("Failed");
          }
        }
      });
    }
  });

  //Add url into the link button
  function Route() {
    $("#download").attr("href", "/download/" + c.filename.split(".")[0] + ".doc");
    $("#modify").attr("href", "/modify/" + c.filename);
    $("#match").attr("href", "/resumetojd/" + c.filename + "/Opening");
  }
  Route();

  //upload english file
  $("#upload-btn").on("click", function() {
    localStorage.name = filename;

    var uploader = new Upload("file-form");
    uploader.Uploadfile(function() {
      setTimeout(function() {
        window.location.href = "/preview";
      }, 1000);
    });
  });
  $(".upload").on("click", function() {
    $("#file").val("");
    $("#progressmsg").html("");
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
      url: "/updateinfo",
      type: "post",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        "filename": c.filename,
        "yamlinfo": {
          "id": $("#titleId").val().trim(),
          "name": $("#titleName").val().trim(),
          "origin": $("#titleOrigin").val().trim(),
        }
      }),
      success: function(response) {
        if (response.result) {
          window.location.reload();
        } else {
          alert("Failed to submit");
        }
      }
    });
  });

  //Get similar person data.
  $.ajax({
    url: "/analysis/similar",
    type: "post",
    data: {
      "doc": document.getElementById("cvContent").innerText
    },
    success: function(response) {
      var datas = response.result;
      for (var i = 0, len = datas.length; i < len; i++) {
        var _index = datas[i];
        var name = _index.name !== "" ? _index.name : _index.id;

        $("#similarContent").append("<div class='similar-item'><a href='/show/" + _index.md_filename + "' target='_blank'>" +
          name + " | " + _index.position + " | " +
          _index.age + " | " + _index.gender + " | " + _index.education + "</a></div>"
        );
      }
    }
  });

  //Write history
  var history = new History();
  history.writeHistory({
    name: $("#titleName").val(),
    filename: c.filename,
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
});
