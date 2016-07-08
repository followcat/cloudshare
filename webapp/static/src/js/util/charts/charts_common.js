define(["jquery"], function($) {

  //获取一个长度为2的数组
  function getArray(xData, yData) {
    var arr = new Array(2);
    arr[0] = xData;
    arr[1] = yData;
    return arr;
  }

  //获取总月数
  function getSumMonth(beginYear, beginMonth, endYear, endMonth) {
    var year = endYear - beginYear;
    var month,
        monthCount;
    if (year < 0) {
      return -1;
    } else {
      if (parseInt(beginMonth) < parseInt(endMonth)) {
        month = endMonth - beginMonth;
      } else {
        month = beginMonth - endMonth;
      }
      monthCount = year * 12 + month;
      return monthCount;
    }
  }

  //类型转换
  function changeTwoDecimal(x) {
    var f_x = parseFloat(x);
    f_x = Math.round(x * 100) / 100;

    var s_x = f_x.toString(),
        pos_decimal = s_x.indexOf(".");

    if (pos_decimal < 0) {
      pos_decimal = s_x.length;
      s_x += ".";
    }
    while (s_x.length <= pos_decimal + 2) {
      s_x += "0";
    }
    return s_x;
  }

  //获取工作时间
  function getWorkTime(time) {
    var workingYear = parseInt(time / 12),
        workingMonth = time % 12,
        workingTime = changeTwoDecimal(workingYear + (workingMonth / 100));
    return workingTime;
  }

  //获取散点数值
  function getScatterData(capacity) {
    var time = 0,
        actpointSum = 0,
        doclenSum = 0;

    for (var i = capacity.length - 1; i >= 0; i--) {
      var obj = capacity[i];
      if (obj.begin !== "" && obj.end !== "") {
        var num = getSumMonth(obj.begin[0], obj.begin[1], obj.end[0], obj.end[1]);
        if (num === -1) {
          continue;
        } else {
          time += num;
          actpointSum += obj.actpoint;
          doclenSum += obj.doclen;
        }
      }
    }

    var workTime = getWorkTime(time);
    if (workTime < 40) {
      return {
        workTime: workTime,
        actpointSum: actpointSum,
        doclenSum: doclenSum
      };
    } else {
      return 0;
    }
  }

  function ChartsCommon() {}

  ChartsCommon.prototype = {
    constructor: ChartsCommon,

    //获取md_id列表
    //return array
    getMdList: function(objList) {
      var list = [],
          md_id = "";
      for (var i = 0, len = objList.length; i < len; i++) {
        md_id = $(objList[i]).attr("href").split("/")[2];
        list.push(md_id);
      }

      return list;
    },

    //处理position数据
    //return object
    processPosition: function(result, searchText) {
      var dataObj = {};
      $.each(result, function(index, data) {
        if (index !== searchText) {
          if (data.length !== 1) {
            dataObj[index] = this;
          }
        }
      });
      return dataObj;
    },

    //能力分布数据
    getScatterDataList: function(result) {
      var dataArray = [],
          actDoc = [];
      for (var i = result.length - 1; i >= 0; i--) {
        var actionPoint = 0,
            docLen = 0,
            objArray = result[i];
        $.each(objArray, function(index, data) {
          actionPoint += data.actpoint;
          docLen += data.doclen;
        });
        actDoc = getArray(actionPoint, docLen);
        dataArray.push(actDoc);
      }
      return dataArray;
    },

    //获取坐标点的数值
    getPointDataList: function(result) {
      var dataArray = [];
      for (var i = result.length - 1; i >= 0; i--) {
        var dataObj = {},
            personObj = result[i],
            capacity = personObj.capacity,
            scatterData = getScatterData(capacity);

        dataObj.fileName = personObj.md;
        dataObj.data = getArray(scatterData.workTime, scatterData.actpointSum);
        dataArray.push(dataObj);
        dataObj = null;
      }
      return dataArray;
    },

    //获取坐标点比例数值
    getProportionPointData: function(result) {
      var dataArray = [];
      for (var i = result.length - 1; i >= 0; i--) {
        var dataObj = {},
            personObj = result[i],
            capacity = personObj.capacity,
            scatterData = getScatterData(capacity),
            pro = (scatterData.actpointSum / scatterData.doclenSum) * 100,
            actdocPro = Math.pow(pro, 3);

        dataObj.fileName = personObj.md;
        dataObj.data = getArray(scatterData.workTime, pro);
        dataArray.push(dataObj);
        dataObj = null;
      }
      return dataArray;
    }
  };

  return ChartsCommon;
});
