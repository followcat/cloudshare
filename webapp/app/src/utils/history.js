'use strict';

//时间格式化
const dateFormat = (fmt, date) => {

  const o = {
    "M+" : date.getMonth() + 1, //月份
    "d+" : date.getDate(), //日
    "h+" : date.getHours(), //小时
    "m+" : date.getMinutes(), //分
    "s+" : date.getSeconds(), //秒
    "q+" : Math.floor((date.getMonth()+3)/3), //季度
    "S" : date.getMilliseconds() //毫秒
  };

  const week = {
    "0" : "/u65e5",
    "1" : "/u4e00",
    "2" : "/u4e8c",
    "3" : "/u4e09",
    "4" : "/u56db",
    "5" : "/u4e94",
    "6" : "/u516d"
  };
  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
  }
  if (/(E+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? "/u661f/u671f" : "/u5468") : "") + week[date.getDay() + ""]);
  }
  for (var k in o) {
    if (new RegExp(`(${k})`).test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : ((`00${o[k]}`).substr(("" + o[k]).length)));
    }
  }
  return fmt;
};

/**
 * 在storage找出id的位置, 未找到返回-1
 * @param  {string} id [简历id]
 * @param  {array} storage [浏览历史记录列表]
 * @return {int} index [返回的索引位置,未找到返回-1]
 */
const findIndexWithId = (id, storage) => {
  storage.forEach((item, index) => {
    if (item.id === id) {
      return index;
    }
  });
  return -1;
};

const History = {
  /**
   * 写入浏览历史
   * @param  {object} object 
   * @return {void}
   */
  write: (object) => {
    let historyStorage = (localStorage.getItem('history') && JSON.parse(localStorage.getItem('history'))) || [];

    console.log(new Date());
    object.time = dateFormat('yyyy-MM-dd hh:mm:ss', new Date());

    const index = findIndexWithId(object.id, historyStorage);
    if (index > -1) {
      historyStorage.splice(index, 1);
    }
    historyStorage.unshift(object);
    localStorage.setItem('history', JSON.stringify(historyStorage));
  },

  /**
   * 读取浏览历史记录
   * @return {void}
   */
  read: () => {
    return (localStorage.getItem('history') && JSON.parse(localStorage.getItem('history'))) || [];
  }

};

module.exports = History;
