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
    $('#match').on('click', function(e){
      e.stopPropagation();
    });
  }
)