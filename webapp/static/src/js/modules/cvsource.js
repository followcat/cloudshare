require.config({
  baseUrl: '/static/',
  paths: {
    jquery: 'lib/js/jquery',
    bootstrap: 'lib/js/bootstrap',
    datetimepicker: 'lib/js/bootstrap-datetimepicker.min',
    datetimepickerCN: 'lib/js/bootstrap-datetimepicker.zh-CN',
    cvdeal: 'src/js/util/cvdeal',
    Upload: 'src/js/util/upload',
    colorgrad: 'src/js/util/colorgrad',
    History: 'src/js/util/history'
  },
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    },
    datetimepicker: {
      deps: ['jquery'],
      exports: 'bootstrap-datetimepicker'
    },
    datetimepickerCN: {
      deps: ['jquery'],
      exports: 'bootstrap-datetimepicker-zh-CN'
    },
    cvdeal: {
      deps: ['jquery'],
      exports: 'cvdeal'
    }
  }
});

require([
  'jquery',
  'bootstrap',
  'datetimepicker',
  'datetimepickerCN',
  'cvdeal',
  'Upload',
  'colorgrad',
  'History'
],function($, bootstrap, datetimepicker, datetimepickerCN, cvdeal, Upload, ColorGrad, History) {

  window.onload = cvdeal.CVdeal();

  $('.form_date').datetimepicker({
    language: 'zh-CN',
      weekStart: 1,
      todayBtn: 1,
      autoclose: 1,
      todayHighlight: 1,
      startView: 2,
      minView: 2,
      forceParse: 0
  });

  $("#tracking-text").on('focus', function() {
    $(this).next().show();
  });

  $("#comment-text").on('focus', function() {
    $(this).next().show();
  });

  $(".collapse").on('click', function() {
    $(this).parent().hide();
  });

  //add label function
  $("#add-label").on('click', function() {
    var display = $(".add-label-box").css("display");

    if (display === 'none') {
      $(this).text("Fold");
      $(".add-label-box").css("display", "table");
    } else {
      $(this).text("Add a Tag");
      $(".add-label-box").css("display", "none");
    }
  });

  function GetFileName() {
    var url = String(window.location.href);
    var arr = url.split("/");
    var filename = arr[arr.length - 1];

    return filename;
  }

  function CheckBlank(val) {
    var reg = /^\s*$/g;
    if (val === "" || reg.test(val)) {
      return true;
    } else {
      return false;
    }
  }

  //Add tag
  $("#add-label-btn").on('click', function() {
    var filename = GetFileName();
    var label_text = $("#label-text").val();
    var current_user = $("#current-id").text();

    if (CheckBlank(label_text)) {
      $(this).attr("disable", false);
      $("#label-text").focus();
    } else {
      $(this).attr("disable", true);
      $.ajax({
        type: 'POST',
        url: '/updateinfo',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          "filename": filename,
          "yamlinfo": {
            "tag": label_text
          }
        }),
        success: function(result) {
          if (result.result) {
            $(".label-item").prepend("<span class='label label-primary' title=" +
              current_user + ">" + label_text + "</span>");
            $("#label-text").val("");
          } else {
            alert("Operation failed");
          }
        }
      });
    }
  });

  //Add tracking massage
  $("#tracking-btn").on('click', function() {
    var filename = GetFileName();
    var tracking_text = $("#tracking-text").val();
    var date = $("#date").val();
    var current_user = $("#current-id").text();

    if (CheckBlank(tracking_text) || date === "") {
      $(this).attr("disable", false);
      $("#tracking-text").focus();
    } else {
      $(this).attr("disable", true);
      $.ajax({
        type: 'POST',
        url: '/updateinfo',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          "filename": filename,
          "yamlinfo": {
            "tracking": {
              "date": date,
              "text": tracking_text
            }
          }
        }),
        success: function(result) {
          if (result.result) {
            $("#tracking-content").prepend("<div class='tracking-item'><p class='content'>" + tracking_text + "</p><em class='commit-info'>" + current_user + " " + date + "</em></div>");
            $("#tracking-text").val("");
          }
        }
      });
    }
  });

  //Add comment
  $("#comment-btn").on('click', function() {
    var filename = GetFileName();
    var comment_text = $("#comment-text").val();
    var current_user = $("#current-id").text();

    if (CheckBlank(comment_text)) {
      $(this).attr("disable", false);
      $("#comment-text").focus();
    } else {
      $(this).attr("disable", true);
      $.ajax({
        type: 'POST',
        url: '/updateinfo',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          "filename": filename,
          "yamlinfo": {
            "comment": comment_text
          }
        }),
        success: function(result) {
          $("#comment-content").prepend("<div class='comment-item'><em class='commit-info'>" + current_user + "</em><p class='content'>" + comment_text + "</p></div>");
          $("#comment-text").val("");
        }
      });
    }
  });

  //Get current url to get file name
  var url = window.location.href.split('/');
  var filename = url[url.length - 1];

  //Add url into the link button
  function Route() {
    $("#download").attr('href', '/download/' + filename.split('.')[0] + '.doc');
    $("#modify").attr('href', '/modify/' + filename);
    $('#match').attr('href', '/resumetojd/' + filename);
  }
  Route();

  //upload english file
  $("#upload-btn").on('click', function() {
    localStorage.name = filename;

    var uploader = new Upload("file-form");
    uploader.Uploadfile(function() {
      setTimeout(function() {
        window.location.href = "/preview";
      }, 1000);
    });
  });
  $(".upload").on('click', function() {
    $("#file").val("");
    $("#progressmsg").html("");
  });

  localStorage.title = $('title').text().split('-')[0];


  //CV Title Data Modify

  //Tranform Title Data Modify status
  $('#tranform-check').click(function() {
    if ($(this).attr('checked')) {
      $(this).removeAttr('checked');
      $('#title-table tbody tr input').attr('disabled', 'disabled');
      $('#title-submit-btn').css('display', 'none');
    } else {
      $(this).attr('checked', 'checked');
      $('#title-table tbody tr input').removeAttr('disabled');
      $('#title-submit-btn').css('display', 'block');
    }
  });


  //Title Button Handle
  $('#title-submit-btn').on('click', function() {
    var filename = window.location.href.split('/');
    filename = filename[filename.length - 1];

    $.ajax({
      url: '/updateinfo',
      type: 'post',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        'filename': filename,
        'yamlinfo': {
          'id': $('#Id').val(),
          'name': $('#name').val(),
          'origin': $('#origin').val()
        }
      }),
      success: function(response) {
        if (response.result) {
          window.location.reload();
        } else {
          alert('Failed to submit');
        }
      }
    });
  });

  //Get similar person data.
  $.ajax({
    url: '/analysis/similar',
    type: 'post',
    data: {
      'doc': document.getElementById("cv-content").innerText
    },
    success: function(response) {
      var datas = response.result,
          colorgrad = ColorGrad();
      for(var i = 0, len = datas.length; i < len; i++){
        var fileName = datas[i][0],
            name = datas[i][1].name,
            match = datas[i][2].match;

        colorStyle = colorgrad.gradient(parseInt(match*100));
        $('#similar-person').append("<a href=\"/show/"+ fileName +
          "\" style=\"color:" + colorStyle +
          "\" target=\"_blank\">" + name + "</a>");
      }
    }
  });

  //Write history
  var history = new History(),
      name = $('#name').val();
  history.writeHistory(name, filename);

});
