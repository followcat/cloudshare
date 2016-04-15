require.config({

  baseUrl: "../static/js",

  paths: {
    'jquery': 'lib/jquery',
    'bootstrap': 'lib/bootstrap',
    'bootstraptable': 'lib/bootstrap-table.min',
    'header': 'src/header',
    'formvalidate': 'src/formvalidate',
    'Upload': 'src/upload'
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
    'bootstrap',
    'bootstraptable',
    'header',
    'formvalidate',
    'Upload'
  ],
  function($){
    //Send company name to modal input
    $('#addJobDescriptionModal').on('show.bs.modal', function (event) {
      $('#job-description-name').val('');
      $('#job-description').val('');

      var button = $(event.relatedTarget); // Button that triggered the modal
      var companyName = button.data('whatever'); // Extract info from data-* attributes

      var modal = $(this);

      modal.find('#jd-company-name').val(companyName);
    });

    //Add company
    $('#save-company').on('click', function(){
      var companyName = $('#company-name').val(),
          introduction = $('#introduction').val();

      $.ajax({
        url: '/addcompany',
        type: 'post',
        data: {
          'name': companyName,
          'introduction': introduction
        },
        success: function(response){
          console.log(response)
        }
      });
    });

    //Add JD
    $('#save-jd').on('click', function(){
      var companyName = $('#jd-company-name').val(),
          jdName = $('#job-description-name').val(),
          jd = $('#job-description').val();

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
            $('#jd-madal-body').append("<div class=\"alert alert-success\" role=\"alert\"><strong>Well done!</strong>You successfully save this job description.<\/div>");
          }else{
            $('#jd-madal-body').append("<div class=\"alert alert-danger\" role=\"alert\"><strong>Fail!</strong>You failed save this job description.<\/div>");
          }
        }
      });
    });
  }
)