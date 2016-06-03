require.config({
  baseUrl: "static/",
  paths: {
    'jquery': 'lib/jquery',
    'bootstrap': 'lib/bootstrap',
    'bootstraptable': 'lib/bootstrap-table.min',
    'header': 'src/js/util/header',
    'formvalidate': 'src/js/util/formvalidate',
    'Upload': 'src/js/util/upload'
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
          if (response.result){
            $('#addCompanyModal').modal('hide');
            $('#message').text('Add company informations success!');
            $('#messageModal').modal('show');
            $('#messageModal').on('hidden.bs.modal', function (e) {
              window.location.reload();
            });
          }else{
            $('#modifyJDModal').modal('hide');
            $('#message').text('Add company informations failed!');
            $('#messageModal').modal('show');
          }
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
            $('#addJobDescriptionModal').modal('hide');
            $('#message').text('You successfully save this job description.');
            $('#messageModal').modal('show');
            $('#messageModal').on('hidden.bs.modal', function (e) {
              window.location.reload();
            });
          }else{
            $('#modifyJDModal').modal('hide');
            $('#message').text('You failed save this job description.');
            $('#messageModal').modal('show');
          }
        }
      });
    });
  }
);
