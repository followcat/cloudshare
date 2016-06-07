require.config({
  baseUrl: "/static/",
  paths: {
    'jquery': 'lib/js/jquery',
    'bootstrap': 'lib/js/bootstrap',
    'bootstraptable': 'lib/js/bootstrap-table.min',
    'header': 'src/js/util/header',
    'formvalidate': 'src/js/util/formvalidate',
    'Upload': 'src/js/util/upload',
    'radarcharts': 'src/js/util/charts/radarcharts'
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
  ],function($, radarcharts){
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
            $('#jd-madal-body').append("<div class=\"alert alert-success\" role=\"alert\">"+
              "<strong>Well done!<\/strong>You successfully save this job description.<\/div>");
            window.location.reload();
          }else{
            $('#jd-madal-body').append("<div class=\"alert alert-danger\" role=\"alert\">"+
              "<strong>Fail!<\/strong>You failed save this job description.<\/div>");
          }
        }
      });
    });

    function replaceName(datas){
      for( var i = 0, datasLen = datas.length; i < datasLen; i++){
        for ( var j = 0, valuesLen = datas[i].value.length; j < valuesLen; j++){
          var name = datas[i].value[j].name;
          name = name.split('');
          if ( name.length === 2) {
            name[1] = '*';
          }else if ( name.length === 3 ) {
            name[1] = '*';
            name[2] = '*';
          }else if ( name.length === 4) {
            name[1] = '*';
            name[2] = '*';
            name[3] = '*';
          }else if ( name.length > 4){
            var temp = name;
            for (var z = temp.length - 1; z >= 3; z--) {
                temp[z] = '';
            }
            name = temp;
            name[1] = '*';
            name[2] = '*';
          }
          name = name.join('');
          datas[i].value[j].name = name;
        }
      }
      return datas;
    }

    //Edit JD button click function
    function bindEditJDEvent(){
      $('.edit-jd').on('click', function(){
        if ($(this).parent().prev().text() === $('#name').text().trim()){
          var jdTd = $(this).parent().parent().find('.jd-td');
          var id = jdTd.attr('data-id');
          $('#change-jd').val(jdTd.text());
          $('#change-jd').attr('data-id', id);
          $('#modifyJDModal').modal('show');
        }else{
          $('#message').text('You can\'t change this job description!');
          $('#messageModal').modal('show');
        }
      });
    }
    //Call Edit JD click function
    bindEditJDEvent();

    //Draw charts button click function
    function bindCVJDEvent(){
      $('.cv-jd-match').on('click', function(){
        $('#chart-wrapper').html('');
        var That = $(this);

        //Closure: send this object
        (function(That){
          setTimeout(function(){
            var radar = radarcharts('chart-wrapper'),
                jd_id = That.parent().parent().find('.jd-td').attr('data-id'),
                title = That.attr('data-filename');

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
                  var datas = replaceName(response.data);
                  radar.makeRadar(datas, response.max);
                }
            });
          }, 500);
        })(That);
      });
    }
    bindCVJDEvent();

    //Bootstrap-table events re-binding
    window.actionEvents = {
      //Draw a charts button events
      "click .cv-jd-match": function(e, value, row, index) {
        $('#chart-wrapper').html('');  //clean
        setTimeout(function(){
          var radar = radarcharts('chart-wrapper'),
              jdId = row["_2_data"].id,
              fileName = $(e.target).attr("data-filename");
          var nameList = [];
          nameList.push(fileName);
          $.ajax({
            url: "/analysis/valuable",
            type: "POST",
            data: {
              "jd_id": jdId,
              "name_list": JSON.stringify(nameList)
            },
            success: function(response){
              var datas = replaceName(response.data);
              radar.makeRadar(datas, response.max);
            }
          });
        }, 500);
      },
      //edit-id button events
      "click .edit-jd": function(e, value, row, index) {
        var creator = row[3];

        if ( creator === $('#name').text().trim() ) {
          var jdContent = row[2],
              jdId = row["_2_data"].id;
          $('#change-jd').val(jdContent);
          $('#change-jd').attr('data-id', jdId);
          $('#modifyJDModal').modal('show');
        } else {
          $('#message').text('You can\'t change this job description!');
          $('#messageModal').modal('show');
        }
      }
    };

    //Change job description button Event
    $('#change-jd-btn').on('click', function(){
      $.ajax({
        url: '/modifyjd',
        type: 'POST',
        data: {
          'id': $('#change-jd').attr('data-id'),
          'description': $('#change-jd').val()
        },
        success: function(response){
          if ( response.result ) {
            $('#modifyJDModal').modal('hide');
            $('#message').text('Change this job description success!');
            $('#messageModal').modal('show');
            $('#messageModal').on('hidden.bs.modal', function (e) {
              window.location.reload();
            });
          }else{
            $('#modifyJDModal').modal('hide');
            $('#message').text('Change this job description failed!');
            $('#messageModal').modal('show');
          }
        }
      });
    });
  }
);
