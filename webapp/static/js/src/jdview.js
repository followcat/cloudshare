require.config({

  baseUrl: "../static/js",

  paths: {
    'jquery': 'lib/jquery',
    'bootstrap': 'lib/bootstrap',
    'bootstraptable': 'lib/bootstrap-table.min',
    'header': 'src/header',
    'formvalidate': 'src/formvalidate',
    'Upload': 'src/upload',
    'radarcharts': 'src/charts/radarcharts'
  },

  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    },
    bootstraptable: {
      deps: ['jquery'],
      exports: 'bootstraptable'
    }
  }

});

require(
  [
    'jquery',
    'radarcharts',
    'bootstrap',
    'bootstraptable',
    'header',
    'formvalidate',
    'Upload'
  ],
  function($, radarcharts){
    $('#match').on('click', function(e){
      e.stopPropagation();
    });

    //Add JD
    $('#save-jd').on('click', function(){
      var companyName = $('#company-name').val(),
          jdName = $('#jd-project-name').val(),
          jd = $('#jd').val();

      $.ajax({
        url: '/addjd',
        type: 'post',
        data: {
          'coname': companyName,
          'jdname': jdName,
          'description': jd
        },
        success: function(response){
          if (response.result){
            $('#jd-madal-body').append("<div class=\"alert alert-success\" role=\"alert\"><strong>Well done!<\/strong>You successfully save this job description.<\/div>");
            window.location.reload();
          }else{
            $('#jd-madal-body').append("<div class=\"alert alert-danger\" role=\"alert\"><strong>Fail!<\/strong>You failed save this job description.<\/div>");
          }
        }
      });
    });

    $('.cv-jd-match').on('click', function(){
      $('#chart-wrapper').html('');
      var That = $(this);

      //闭包传递this对象
      (function(That){
        setTimeout(function(){

          var radar = radarcharts('chart-wrapper'),
              jd_id = That.prev().attr('href').split('=')[1],
              title = That.attr('title');

          var name_list = [];
          name_list.push(title);

          $.ajax({
              url: '/analysis/valuable',
              type: 'post',
              data: {
                  'jd_id': jd_id,
                  'name_list': JSON.stringify(name_list)
              },
              success: function(response) {
                  radar.makeRadar(response.data, response.max);
              }
          });

        }, 500);

      })(That);
    
    });
  }
)