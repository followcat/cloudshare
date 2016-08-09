require.config({
  baseUrl: "/static/",

  paths: {
    jquery: "lib/js/jquery",
    bootstrap: "lib/js/bootstrap",
    cvdeal: "src/js/util/cvdeal",
    Upload: "src/js/util/upload",
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

  window.onload = cvdeal.cvDeal("cvContent");

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
    var nameValue = $("#resumeName").val().trim(),
        sourceValue = $("#originSelection").val();
    
    if (nameValue !== "") {
      $.ajax({
        url: "/confirm",
        type: "POST",
        data: {
          "name": nameValue,
          "origin": sourceValue
        },
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
    } 
  });

  $("#goBackBtn").on("click", function() {
    history.go(-1);
  });
});