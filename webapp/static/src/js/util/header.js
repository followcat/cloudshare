define(['jquery', 'formvalidate', 'Upload'], function($, formvalidate, Upload){

  var header = {};

  //upload event
  header.UploadHandle = function(objBtn){
    objBtn.on('click', function(){
      localStorage.name = "";
      var uploader = new Upload("file-form");
      uploader.Uploadfile(function(){
        setTimeout(function(){
          window.location.href = "/uppreview";
        }, 1000);
      });
    });
  };
  header.UploadHandle($("#upload-btn"));

  // Login out in header
  header.LogOut = function(obj){
    //obj is a element object
    obj.on("click", function(event){
      $.ajax({
        url: '/api/session',
        type: 'DELETE',
        success: function(response){
          if (response.code === 200) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = "/";
          } else {
            alert(response.message);
          }
        },
        error: function(msg){
          alert("Operate Error!");
        }
      });
      event.preventDefault();    //prevent event default.
    });
  };
  header.LogOut($("#quit-btn"));

  //setting in header
  header.Setting = function(objBtn, objForm, msgBox){
    objBtn.on('click', function(){
      var aPwd = objForm.find(":password");
      if(!formvalidate.ValidateBlank(aPwd)){
        //change password, send request
        $.ajax({
          url: objForm.attr('action'),
          type: objForm.attr('method'),
          dataType: 'text',
          data: objForm.serialize(),
          success: function(result){
            var resultJson = $.parseJSON(result);
            if(resultJson.result){
              msgBox.text("The password is changed, please login again.");
              setTimeout(function(){
                window.location.href = "/";
              },2000);
            }else{
              msgBox.text("Operation Failed!");
            }
          },
          error: function(msg){
            alert("Error!");
          }
        });
      }
      event.preventDefault();
    });
  };
  header.Setting($("#cpwd-btn"), $("#cpwd-form"), $("#error-msg"));

  //set button is disable
  header.DisableBtn = function(obj){
    obj.attr("disabled",true);
  };

  //set button is able
  header.AbleBtn = function(obj){
    obj.attr("disabled",false);
  };

  //password input validate
  header.ValidatePwd = function(objOldPwd, objNewPwd, objCfPwd, objCPwdBtn, msgBox){
    //newpassword input validate
    objOldPwd.on('blur', function(){
      if(!formvalidate.ValidatePassword(this.value)){
        header.DisableBtn(objCPwdBtn);   //if illegal disable button
        msgBox.text("illegal password. At least 6-12 strings");
      }else{
        header.AbleBtn(objCPwdBtn);
        msgBox.text("");
      }
    });

    objNewPwd.on('blur', function(){
      if(!formvalidate.ValidatePassword(this.value)){
        header.DisableBtn(objCPwdBtn);
        msgBox.text("illegal password. At least 6-12 strings");
      }else{
        header.AbleBtn(objCPwdBtn);
        msgBox.text("");
      }
    });

    objCfPwd.on('blur', function(){
      var cofpwd = $(this);
      var cofpwdVal = this.value;

      //judge the input value
      if(!formvalidate.ValidatePassword(cofpwdVal)){
        header.DisableBtn(objCPwdBtn);
        msgBox.text("illegal confirm password. At least 6-12 strings");
      }else{
        var pwdVal = $(cofpwd.attr("data-compare")).val();

        if(!formvalidate.ComparePassword(pwdVal, cofpwdVal)){
          header.AbleBtn(objCPwdBtn);
          msgBox.text("The passwords you entered do not match. Please re-enter your passwords. ");
        }else{
          header.AbleBtn(objCPwdBtn);
          msgBox.text("");
        }
      }
    });
  };
  header.ValidatePwd($("#oldpassword"), $("#newpassword"), $("#confirmpassword"), $("#cpwd-btn"), $("#error-msg"));

  header.UploadDiv = function(obj){
    obj.on('click', function(){
      $("#file").val("");
      $("#progressmsg").html("");
    });
  };
  header.UploadDiv($(".upload"));

  header.getModelList = function() {
    $.ajax({
      url: "/modellist",
      type: "POST",
      success: function(response) {
        var data = response.model_list,
            model = localStorage.model ? localStorage.model : '';

        for (var i = 0, len = data.length; i < len; i++) {
          if (model === data[i] && model !== "") {
            $("#modelMenu").append("<p>"+ data[i] +"</p>");
          } else {
            $("#modelMenu").append("<p>"+ data[i] +"</p>");
          }
        }
      }
    })
  };
  header.getModelList();

  header.modelItemEvent = function() {
    $("#modelMenu").delegate(".model-item", "click", function() {
      var _this = $(this);
      if (_this.attr("data-flag") === "true") {
        _this.attr("data-flag", "false");
        localStorage.model = "";
        _this.find(".glyphicon").remove();
      } else {
        var models = $(".model-item");
        for (var i = 0, len = models.length; i < len; i++) {
          $(models[i]).attr("data-flag", "false");
          $(models[i]).find(".glyphicon").remove();
        }
        localStorage.model = _this.text();
        _this.attr("data-flag", "true");
        _this.append("<span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>");
      }
    });
  };
  header.modelItemEvent();

  return header;
});
