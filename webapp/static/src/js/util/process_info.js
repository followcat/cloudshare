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
        $elementName = $(".age");
    processInfo.addName($elementName);
    processInfo.deleteSquareBrackets($elementName);

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
        _this.parent().find('.experience-hide').css({'display': 'block'});
        _this.text('Fold');
      } else {
        _this.parent().find('.experience-hide').css({'display': 'none'});
        _this.text('Unfold');
      }
    });
  }();
});
