define(['../js/lib/js.cookie-2.1.1.min'], function(jsCookie){

  function Cookies(){
  }

  Date.prototype.pattern = function(fmt){
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
    if(/(y+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    if(/(E+)/.test(fmt)){
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(fmt)){
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
        }
    }
    return fmt;
  };

  Cookies.prototype.writeCookie = function(name, fileName){
    var new_view_array = [],
        new_cookie = {},
        user_view = jsCookie.get('history');

    if ( !user_view ) {
      new_cookie.name = name;
      new_cookie.fileName = fileName;
      new_cookie.time = new Date().pattern('yyyy-MM-dd hh:mm:ss');
      new_view_array.push(new_cookie);
    } else {
      user_view = JSON.parse(user_view);
      for ( var i = 0, len = user_view.length; i < len; i++ ) {
        if ( user_view[i].name !== name && user_view[i].fileName !== fileName ) {
          new_view_array.push(user_view[i]);
        }
      }

      new_cookie.name = name;
      new_cookie.fileName = fileName;
      new_cookie.time = new Date().pattern('yyyy-MM-dd hh:mm:ss');
      new_view_array.push(new_cookie);
    }

    jsCookie.set('history', JSON.stringify(new_view_array), { expires: 7, path: '/' });
  };

  Cookies.prototype.readCookie = function(){
    var cookieLists = jsCookie.get('history');
    if ( cookieLists ) {
      cookieLists = JSON.parse(cookieLists);
    }
    return cookieLists;
  };

  return Cookies;
});
