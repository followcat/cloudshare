/*
  @description: 浏览历史读写
  @author: Junkai Chen
  @email: chenjunkai1024@outlook.com
*/
define( function(){
  'use strict'

  function pushNewItem(object, itemArray) {
    var historyObject = {};
    for ( var e in object) {
      historyObject[e] = object[e];
    }
    historyObject.time = new Date().pattern('yyyy-MM-dd hh:mm:ss');
    itemArray.push(historyObject);
    return itemArray;
  }

  function History() {
  }

  //时间格式化
  Date.prototype.pattern = function(fmt) {
    var o = {
      "M+" : this.getMonth()+1, //月份
      "d+" : this.getDate(), //日
      "h+" : this.getHours(), //小时
      "m+" : this.getMinutes(), //分
      "s+" : this.getSeconds(), //秒
      "q+" : Math.floor((this.getMonth()+3)/3), //季度
      "S" : this.getMilliseconds() //毫秒
    };
    var week = {
      "0" : "/u65e5",
      "1" : "/u4e00",
      "2" : "/u4e8c",
      "3" : "/u4e09",
      "4" : "/u56db",
      "5" : "/u4e94",
      "6" : "/u516d"
    };
    if (/(y+)/.test(fmt)) {
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    if (/(E+)/.test(fmt)) {
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);
    }
    for (var k in o) {
        if (new RegExp("("+ k +")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
        }
    }
    return fmt;
  };

  /*
    @function: 写入浏览历史
    @params: object
  */
  History.prototype.writeHistory = function(object) {
    var newViewArray = [],
        historyStorage = localStorage.getItem('history') ? localStorage.getItem('history') : null;

    if ( !historyStorage ) {
      newViewArray = pushNewItem(object, newViewArray);
    } else {
      historyStorage = JSON.parse(historyStorage);

      for ( var i = 0, len = historyStorage.length; i < len; i++ ) {
        var diff = true;
        for (var v in historyStorage[i]) {
          if (historyStorage[i][v] === object[v]) {
            diff = false;
          }
        }
        if (diff) {
          newViewArray.push(historyStorage[i]);
        }
      }
      newViewArray = pushNewItem(object, newViewArray);
    }

    localStorage.setItem('history', JSON.stringify(newViewArray));
  };

  /*
    @function: 读取浏览历史记录
    @return: array
  */
  History.prototype.readHistory = function() {
    return localStorage.getItem('history') ? JSON.parse(localStorage.getItem('history')) : [];
  };

  return History;
});
