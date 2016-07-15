define(["jquery"], function() {
  function ProcessInfo() {}

  ProcessInfo.prototype = {
    constructor: ProcessInfo,

    //候选人信息列表加入名字
    addName: function(elements) {
      for (var i = elements.length - 1; i >= 0; i--) {
        var oName = $(elements[i]),
            nameBox = oName.find("span"),
            nameText = nameBox.text();

        var title = "",
            name = "";
        if (nameText === "") {
          title = oName.parent().parent().prev().find("a").text();
          name = title.split("-")[0];
          nameBox.text(name);
        }
      }
    },

    //处理年龄显示为[]
    deleteSquareBrackets: function(elements) {
      for (var i = elements.length - 1; i >= 0; i--) {
        var oAge = $(elements[i]),
            ageBox = oAge.find("span"),
            ageText = ageBox.text();

        if (ageText === "[]") {
          ageBox.text("");
        }
      }
    },

    //折叠 点击事件函数
    toggle: function(obj) {
      obj.on("click", function() {
        var _this = $(this),
            oBlock = _this.next();

        if (_this.children().text() === "+") {
          _this.children().text("-");
          oBlock.show();
          obj.flag = true;
        } else {
          _this.children().text("+");
          oBlock.hide();
          _this.flag = false;
        }
      });
    },

    //增加信息事件
    addInfoHandler: function(obj) {
      var nextBrother = obj.next();
      if (nextBrother.css("display") === "none") {
        obj.children("span").text("-");
        nextBrother.show();
      } else {
        obj.children("span").text("+");
        nextBrother.hide();
      }
    }
  };

  return function() {
    var processInfo = new ProcessInfo();

    var $elementName = $(".name"),
        $elementAge = $(".age");
    processInfo.addName($elementName);
    processInfo.deleteSquareBrackets($elementAge);

    //调用折叠函数
    processInfo.toggle($(".label-alink"));
    processInfo.toggle($(".comment-alink"));

    //跟进点击事件
    $(".tracking-link").on("click", function() {
      processInfo.addInfoHandler($(this));
    });
    //评论点击事件
    $(".comment-link").on("click", function() {
      processInfo.addInfoHandler($(this));
    });

    //显示更多的工作经历点击事件
    $(".show-more").on("click", function() {
      var _this = $(this),
          $text = _this.text();

      if ($text.indexOf('Unfold') !== -1) {
        _this.parent().find('.ex-fold').css({'display': 'block'});
        _this.text('Fold');
      } else {
        _this.parent().find('.ex-fold').css({'display': 'none'});
        _this.text('Unfold');
      }
    });

    //结果列表字段定位
    var headerHeigth = $("header").innerHeight(),
        toolWrapHeight = $(".tool-bar-wrap").outerHeight() + parseInt($(".tool-bar-wrap").css("marginTop"));
    $(document).scroll( function() {
      var top = $(document).scrollTop();
      if (top > headerHeigth + toolWrapHeight) {
        $(".field").addClass("top-fixed");
      } else {
        $(".field").removeClass("top-fixed");
      }
    });

    //顶部工具容器折叠事件
    var initToolWrapHeight = $(".tool-bar-wrap").outerHeight();
    $("#toolWrapUpDown").on("click", function() {
      var $iconElement = $(this).children("span");
      if ($(this).attr("data-flag") === "true") {
        $iconElement.removeClass("glyphicon-chevron-down");
        $iconElement.addClass("glyphicon-chevron-up");
        $(".tool-bar-wrap").css({
          'height': 'auto',
          'overflow': 'inherit'
        });
        $(this).attr("data-flag", "false");
      } else {
        $iconElement.removeClass("glyphicon-chevron-up");
        $iconElement.addClass("glyphicon-chevron-down");
        $(".tool-bar-wrap").css({
          'height': initToolWrapHeight + 'px',
          'overflow': 'hidden'
        });
        $(this).attr("data-flag", "true");
      }
    });
  }();
});
