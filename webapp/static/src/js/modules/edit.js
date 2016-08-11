require.config({
  baseUrl: '/static/',
  paths: {
    jquery: 'lib/js/jquery',
    cvdeal: 'src/js/util/cv_deal'
  },
  shim: {
    cvdeal: {
      deps: ['jquery'],
      exports: 'cvdeal'
    }
  }
});

require(['jquery', 'cvdeal'], function($, cvdeal){

  window.onload = cvdeal.CVdeal();

  function Edit(obj){
    obj.on('dblclick', function(){
      if(!$(this).children().is('textarea')){
        $(this).find('#delete').remove();
        var text = $(this).html();
        $(this).html("<textarea cols='24' wrap='hard'>" + text + "</textarea>");

        $(this).find('textarea').focus().on('blur', function(){
          var val = $(this).val();
          $(this).parent().html(val);
        });
      }
    });

    obj.on('mouseenter', function(){
      $(this).append("<button type='button' id='delete' class='close'><span aria-hidden='true'>&times;</span></button>");
      $(this).find("#delete").css({
        'position' : 'absolute',
        'right' : '0',
        'top' : '0'
      }).on('click', function(){
        $(this).parent().remove();
      });
    });

    obj.on('mouseleave', function(){
      $(this).find('#delete').remove();
    });
  }

  var oTd = $("td"),
      oP = $("p");
  Edit(oTd);
  Edit(oP);

  var content = $('#cv-box').html(),
      obj = $(content);

  $('#exports-btn').click(function() {
    var content = $('#cv-content').html(),
        header = $("header").html(),
        style = $("style").html(),
        meta = "<meta charset='utf-8'>";
    var html = meta + "<style>" + style + "</style>" +
              "<header class='header-box'>" + header + "</header>" +
              "<div id='cv-box'><div id='cv-content'>" + content + "</div></div>";
    var filename = $('title').text();

    var link = document.createElement('a');
    mimeType = 'text/html';
    link.setAttribute('download', filename);
    link.setAttribute('href', 'data:' + mimeType  +  ';charset=utf-8,' + encodeURIComponent(html));
    link.click();
  });

  function setTitle(){
    var title = localStorage.title;
    localStorage.removeItem('title');
    $('title').text(title);
  }
  setTitle();

  function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL;
  }

  //logo image to base64
  $('.logo')[0].src = getBase64Image($('.logo')[0]);

});
