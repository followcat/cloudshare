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

require(['jquery', 'bootstrap', 'header', 'formvalidate', 'Upload'], function($) {
  var height = $(window).height() - $("header").height();
  $("#result").height(height - 4);
  $('#check').on('click', function() {
    $('#result').html('');
    $.ajax({
      url: '/analysis/lsi',
      type: 'post',
      data: {
        'doc': $('textarea').val()
      },
      success: function(response) {
        var data = response.result;
        for (var i = 0, len = data.length; i < len; i++) {
          var htmlStr = '';
          htmlStr = "<div class='result-item'>" +
            "<p>匹配值: " + data[i].str + "</p>" +
            "<div class='title'><a href='/show/" + data[i].filename + "' target='_blank'>" + data[i].yaml['name'] + "</a></div>" +
            "<ul class='list-unstyled clearfix'>" +
            "<li><strong>姓名:</strong>" + data[i].yaml['name'] + "</li>" +
            "<li><strong>年龄:</strong>" + data[i].yaml['age'] + "</li>" +
            "<li><strong>学历:</strong>" + data[i].yaml['education'] + "</li>" +
            "<li><strong>院校:</strong>" + data[i].yaml['school'] + "</li>" +
            "<li><strong>职位:</strong>" + data[i].yaml['position'] + "</li>" +
            "<li><strong>公司:</strong>" + data[i].yaml['company'] + "</li>" + "</ul>" +
            "</div>";
          $('#result').append(htmlStr);
        }
      }
    });
  });
});
