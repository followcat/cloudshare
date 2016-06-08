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

    //编辑JD模块封装
    function EditJD(jdId, jdContent, companyName, creator, userName) {
      this.jdId = jdId,
      this.jdContent = jdContent,
      this.companyName = companyName,
      this.userName = userName,
      this.creator = creator
    }

    EditJD.prototype.setValue = function(){
      $("input[name='companyName']").val(this.companyName);
      $("input[name='jdId']").val(this.jdId);
      $("textarea[name='jdContent']").val(this.jdContent);
      if( this.userName === this.creator ) {
        $("#changeJDBtn").removeAttr("disabled");
      } else {
        $("#changeJDBtn").attr("disabled", "disabled");
      }
    }

    //Edit JD button click function
    function bindEditJDEvent(){
      $('.edit-jd').on('click', function(){
        var selfParentTR = $(this).parent().parent();
        var tdElements = selfParentTR.find("td");

        var companyName = $(tdElements[0]).text(),
            jdId = $(tdElements[2]).attr("data-id"),
            jdContent = $(tdElements[2]).attr("title"),
            creator = $(tdElements[3]).text(),
            userName = $("#name").text().trim();

        var editJdObj = new EditJD(jdId, jdContent, companyName, creator, userName);
        editJdObj.setValue();
        $('#modifyJDModal').modal('show');
      });
    }
    //Call Edit JD click function
    bindEditJDEvent();


    //Draw charts button click function
    function bindCVJDEvent(){
      $('.cv-jd-match').on('click', function(){
        var selfParentTR = $(this).parent().parent();
        var tdElements = selfParentTR.find("td");
        var jdContent = $(tdElements[2]).attr("title");

        $("textarea[name='jdModalContent']").attr("data-filename", $(this).attr("data-filename"));
        $("textarea[name='jdModalContent']").val(jdContent);
        $("#JDModal").modal("show");
      });
    }
    bindCVJDEvent();

    //CV JD Matching
    $("#CVJDSubmit").on("click", function(){
      $('#chart-wrapper').html('');
      $("#radarModal").modal("show");
      setTimeout(function(){
        var radar = radarcharts('chart-wrapper'),
            textareaObj = $("textarea[name='jdModalContent']");

        var name_list = [],
            jdContent = textareaObj.val(),
            fileName = textareaObj.attr("data-filename");
        name_list.push(fileName);

        $.ajax({
            url: '/analysis/valuable',
            type: 'post',
            data: {
              'jd_doc': jdContent,
              'name_list': JSON.stringify(name_list)
            },
            success: function(response) {
              var datas = replaceName(response.data);
              radar.makeRadar(datas, response.max);
            }
        });
      }, 500);
    });

    //Bootstrap-table events re-binding
    window.actionEvents = {
      //Draw a charts button events
      "click .cv-jd-match": function(e, value, row, index) {
        $("textarea[name='jdModalContent']").val(row["_2_title"]);
        $("textarea[name='jdModalContent']").attr("data-filename", e.currentTarget.attributes["data-filename"].value);
        $("#JDModal").modal("show");
      },
      //edit-id button events
      "click .edit-jd": function(e, value, row, index) {
        var companyName = row[0],
            jdId = row["_2_data"].id,
            jdContent = row[2],
            creator = row[3],
            userName = $("#name").text().trim();
        var editJdObj = new EditJD(jdId, jdContent, companyName, creator, userName);
        editJdObj.setValue();
        $('#modifyJDModal').modal('show');
      }
    };

    //Change job description button Event
    $('#changeJDBtn').on('click', function(){

      $.ajax({
        url: '/modifyjd',
        type: 'POST',
        data: {
          "id": $("input[name='jdId']").val(),
          "description": $("textarea[name='jdContent']").val(),
          "status": $("#statusSelect").val()
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

});
