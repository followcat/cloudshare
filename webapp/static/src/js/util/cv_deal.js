define(['jquery'], function() {

  //获取字符串hash值
  function hashcode(str) {
    var hash = 0, i, chr, len;
    if (str.length === 0) return hash;
    for (i = 0, len = str.length; i < len; i++) {
      chr   = str.charCodeAt(i);
      hash  = ((hash << 5) - hash) + chr;
      hash |= 0; // Convert to 32bit integer
    }
    return hash;
  }

  //判断当前节点的子节点是否存在table标签,若存在返回true
  function isTableTagExisted(obj) {
    var childNodeList = obj.children;
    for (var i = 0, len = childNodeList.length; i < len; i++) {
      if (childNodeList[i].nodeName === "TABLE") {
        return true;
      }
    }
    return false;
  }

  //在文字内容中加入<br>
  function addBrOnText(obj) {
    var oText = obj.text(),
        patternChinese = /[\u4e00-\u9fa5]{15,}/,
        patternLine = /-{3,}/g;
        br1 = /；|;/g,
        br2 = /。/g;

    if (patternLine.test(oText)) {
      oText = oText.replace(patternLine, "");
      obj.text(oText);
    }

    if (patternChinese.test(oText)) {
      oText = oText.replace(br1, "；<br />");
      oText = oText.replace(br2, "。<br />");
      obj.html(oText);
    }
  }

  //定义CV处理类
  function CVDeal(cv, callback) {
    this.cv = cv;
    this.callback = callback;
  }

  //删除hr标签
  CVDeal.prototype.deleteHrTag = function() {
    var oHr = this.cv.find("hr");
    if (oHr.length > 0) {
      oHr.remove();
    }
  };

  //删除内容为类似"---"横线的section标签
  CVDeal.prototype.deleteSectionTag = function() {
    var reg = /section-\d+|section/,
        oH2 = this.cv.find("h2");
    oH2.each(function() {
      if (reg.test(this.id)) {
        this.remove();
      }
    });
  };

  //删除段落中的链接
  CVDeal.prototype.deleteLink = function() {
    var reg = /[\u4e00-\u9fa5]+/,
        childP = this.cv.find("p");
    childP.each(function() {
      var a = $(this).children("a");
      var a_text = a.text();
      if (reg.test(a_text) && a_text !== "") {
        a.remove();
      }
    });
  };

  //删除横线
  CVDeal.prototype.deleteLine = function() {
    var pattern = /-{3,}/g,
        allElementP = this.cv.find("p"),
        allElementTh = this.cv.find("th"),
        allElementTd = this.cv.find("td");

    allElementTh.each(function() {
      var text = $(this).text();
      if (pattern.test(text)) {
        $(this).parent().remove();
      }
    });

    allElementP.each(function() {
      var _this = $(this);
      var reg = /^(&nbsp;)(&nbsp;)*(&nbsp;)$/;

      if (reg.test(_this.html())) {
        _this.remove();
      }
      addBrOnText(_this);
    });

    allElementTd.each(function() {
      addBrOnText($(this));
    });
  };

  CVDeal.prototype.concatTd = function() {
    var allElementTd = this.cv.find("td");
    allElementTd.each(function() {
      var _this = $(this);
      if (_this.next().html() === "") {
        _this.next().remove();
        _this.attr("colspan", "2");
      }
    });
  };

  CVDeal.prototype.refactorTable = function() {
    var tableList = $(this.cv)[0].getElementsByTagName("table"),
        htmlArray = [];

    if (tableList.length > 0) {
      for (var i = 0, tableLen = tableList.length; i < tableLen; i++) {
        var tdListOnTable = tableList[i].getElementsByTagName("td"),
            isExisted = false;
        for (var j = 0, tdLen = tdListOnTable.length; j < tdLen; j++) {
          if (isTableTagExisted(tdListOnTable[j])) {
            isExisted = true;
            break;
          } else {
            isExisted = false;
          }
        }

        if (!isExisted) {
          var htmlObj = {
            "hash": "",
            "html": "",
          };
          htmlObj.hash = hashcode(tableList[i].outerHTML.toString().trim());
          htmlObj.html = tableList[i].outerHTML.toString().trim();
          htmlArray.push(htmlObj);
        }
      }

      var htmlStr = "";
      for (var i = 0, len = htmlArray.length; i < len; i++) {
        htmlStr += htmlArray[i].html;
      }

      $(this.cv)[0].innerHTML = htmlStr;
    }

    if (this.callback && typeof this.callback === "function") {
      this.callback();
    }
  };

  CVDeal.prototype.deleteTableAttribute = function() {
    var tableList = $(this.cv)[0].getElementsByTagName("table");
    if (tableList.length > 0) {
      for (var i = 0, len = tableList.length; i < len; i++) {
        tableList[i].removeAttribute("width");
        tableList[i].removeAttribute("style");
      }
    }
  };

  return {
    cvDeal: function(elementId, callback) {
      var objCV = new CVDeal($("#" + elementId), callback);
      objCV.refactorTable();
      objCV.deleteTableAttribute();
      objCV.deleteHrTag();
      objCV.deleteSectionTag();
      objCV.deleteLink();
      objCV.deleteLine();
      objCV = null;
      $("#" + elementId).show();
    }
  }
});