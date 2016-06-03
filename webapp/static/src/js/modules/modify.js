require.config({
  baseUrl: '/static/',
  paths: {
    jquery: 'lib/js/jquery',
    marked: 'lib/js/marked'
  },
  shim: {
    marked: {
      exports: 'marked'
    }
  }
});

require(['jquery', 'marked'], function($, marked){
  var height = $(window).height() - $("header").height();

  // set wrap height
  $("textarea").height(height - 6);
  $("#preview").height(height);

  //transform for markdown
  function TextToMd(textWrap, mdWrap){
    //get textarea value
    var text = textWrap.val();
    mdWrap.html(marked(text));
  }
  TextToMd($('textarea'), $('#preview'));

  //add textarea change handle
  $("textarea").change(function(){
    TextToMd($(this), $('#preview'));
  });

  function AddElement(str, func){
  $('header').append(str);
    func();
  }

  var button = "<button type='button' class='btn btn-default' id='close-btn'>关闭</button>" +
    "<button type='button' class='btn btn-default' id='save-btn'>保存</button>" +
    "<button type='button' class='btn btn-default' id='preview-btn'>预览</button>";

  AddElement(button, function(){
    //set button style
    $('header').find('button').css({
      'float' : 'right',
      'margin-right' : '20px',
      'margin-top' : '8px'
    });

    //add button handle
    /*close window handle*/
    $('#close-btn').on('click', function(){
      window.close();
    });
    /*preview changing*/
    $('#preview-btn').on('click', function(){
      var str = "<form method='POST' action='/preview' id='gopreview' style='display:none;'>" +
        "<textarea name='mddata'>" + $('textarea').val() + "</textarea>" + "</form>";
      $('body').append(str);
      $('#gopreview').attr('target', '_blank');
      $('#gopreview').submit();
      $('#gopreview').remove();
    });
    /*save changing*/
    $('#save-btn').on('click', function(){
      var url = window.location.href.split('/');
      var filename = url[url.length-1];

      $.ajax({
        url: '/modify/' + filename,
        type: 'POST',
        data: {
          'mddata': $('textarea').val()
        },
        success: function(response){
          if(response === 'True'){
            alert('保存成功');
          }else{
            alert('保存失败');
          }
        }
      });
    });
  });
});
