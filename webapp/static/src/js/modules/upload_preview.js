require.config({
  baseUrl: "/static/",

  paths: {
    jquery: "lib/js/jquery",
    bootstrap: "lib/js/bootstrap",
    cvdeal: "src/js/util/cv_deal",
    Upload: "src/js/util/upload",
    header: "src/js/util/header",
    formvalidate: "src/js/util/formvalidate",
  },

  shim: {
    bootstrap: {
      deps: ["jquery"],
      exports: "bootstrap"
    },
    cvdeal: {
      deps: ["jquery"],
      exports: "cvdeal"
    },
  }
});

require([
  "jquery",
  "cvdeal",
  "Upload",
  "bootstrap"
], function($, cvdeal, Upload) {

  cvdeal.cvDeal("cvContent", function() {
    $("#loading").css("display", "none");
  });

  //获取source的数据
  $.ajax({
    url: "/static/origindata.json",
    type: "GET",
    dataType: "json",
    success: function(datas) {
      var len = datas.length;
      if (len > 0) {
        for (var i = 0; i < len; i++) {
          $("#originSelection").append("<option value=\""+ datas[i].origin +"\">"+ datas[i].origin +"</option>")
        }
      } else {
        console.log("No source data.");
      }
    }
  });

  $("#confirmBtn").on("click", function() {
    var nameValue = $("#resumeName").length > 0 ? $("#resumeName").val().trim() : null,
        sourceValue = $("#originSelection").length > 0 ? $("#originSelection").val() : null,
        _id = localStorage.name ? localStorage.name : null,
        postURL = "",
        postData = null;

    if (_id !== "") {
      postURL = "/confirmenglish";
      postData = {
        "name": _id
      };
    } else {
      postURL = "/confirm";
      postData = {
        "name": nameValue !== "" ? nameValue : $("#resumeName").focus(),
        "origin": sourceValue
      };
    }

    $.ajax({
      url: postURL,
      type: "POST",
      data: postData,
      success: function(response) {
        console.log(response);
        if (response.result) {
          setTimeout(function() {
            window.location.href = "/show/" + response.filename;
          }, 500);
        } else {
          alert("This resume is existent or this resume hasn't a contact information.");
        }
      }
    });
  });

  $("#goBackBtn").on("click", function() {
    history.go(-1);
  });
});