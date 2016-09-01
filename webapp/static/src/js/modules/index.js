require.config({
  baseUrl: "/static/",
  paths: {
    jquery: 'lib/js/jquery',
    formvalidate: 'src/js/util/formvalidate',
    bootstrap: 'lib/js/bootstrap',
    marked: 'lib/js/marked'
  },
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    },
    marked: {
      exports: 'marked'
    }
  }
});

require(['jquery', 'formvalidate', 'marked', 'bootstrap'], function($, formvalidate, marked, bootstrap){
  var msg_box = $(".login-msg");

  $("#userInput").on("blur", function(){
    var value = this.value;
    //illegal string
    if(!formvalidate.ValidateAccount(value)){
      msg_box.text("Invalid User Name");
    }else{
      msg_box.text("");
    }
  });

  $("#passwordInput").on("blur", function(){
    var value = this.value;
    if(!formvalidate.ValidatePassword(value)){
      msg_box.text("Invalid Password (At least 6-12 characters)");
    }else{
      msg_box.text("");
    }
  });

  $("#feature-btn").on('click', function(){
    var text = $("#textarea").val();
    $("#preview").html(marked(text));
  });

  $("#loginBtn").on("click", function() {
    var username = $("#userInput").val(),
        password = $("#passwordInput").val();

    $.ajax({
      url: "/login/check",
      type: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      dataType: "json",
      data: JSON.stringify({
        username: username,
        password: password,
      }),
    });
  });
});
