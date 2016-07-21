require.config({
  baseUrl: "/static/",
  paths: {
    "jquery": "lib/js/jquery",
    "bootstrap": "lib/js/bootstrap",
    "header": "src/js/util/header",
    "formvalidate": "src/js/util/formvalidate",
    "Upload": "src/js/util/upload",
    "barcharts": "src/js/util/charts/barcharts",
    "scatters": "src/js/util/charts/scattercharts",
    "History": "src/js/util/history",
    "ChartsCommon": "src/js/util/charts/charts_common",
    "ProcessInfo": "src/js/util/process_info"
  },
  shim: {
    bootstrap: {
      deps: ["jquery"],
      exports: "bootstrap"
    }
  }
});

require(
  [
    "jquery",
    "barcharts",
    "scatters",
    "History",
    "ChartsCommon",
    "bootstrap",
    "header",
    "formvalidate",
    "Upload",
    "ProcessInfo"
  ], function($, Barcharts, Scatters, History, ChartsCommon) {
    'use strict'

    var chartsCommon = new ChartsCommon();

    var pageConstant = {
      $searchTextValue: $("#searchText").val(),
      getDataErrorMessage: "无法获取到数据......",
      $itemObjList: $(".item-title"),
      /*
        @function: 清空容器内容
        @params: string(element id)
      */
      removeContent: function() {
        var $idStr = "";
        for (var i = 0, len = arguments.length; i < len; i++) {
          $idStr = "#" + arguments[i];
          $($idStr).html("");
        }
      }
    };

    //职位情况-柱状图
    $("#vdPosition").on("click", function() {
      $("#chartsModal").modal("show");
      pageConstant.removeContent("echartWrap", "actionMsg");  //清空绘制容器

      setTimeout(function() {
        var barchart = Barcharts("echartWrap");
        $.ajax({
          url: "/mining/position",
          type: "POST",
          data: {
            "search_text": pageConstant.$searchTextValue
          },
          success: function(response) {
            if (response.result !== "") {
              var dataArray = chartsCommon.processPosition(response.result, pageConstant.$searchTextValue);
              barchart.makeBar(dataArray);
              barchart.charts.on("click", function(params) {
                // $("#actionMsg").html("");
                var name = params.name,
                    str = "";
                for (var index in dataArray) {
                  if (name === index) {
                    str += "与<b>" + name + "</b>相关的人选:";
                    for (var i = 0, len = dataArray[index].length; i < len; i++) {
                      var link;
                      for (var filename in dataArray[index][i]) {
                        if (dataArray[index][i][filename].name !== "") {
                          str += "<a href=\"/show/" + filename + "\" target=\"_blank\">" + dataArray[index][i][filename].name + "</a>";
                        } else {
                          str += "<a href=\"/show/" + filename + "\" target=\"_blank\">-[" + filename + "]</a>";
                        }
                      }
                    }
                  }
                }
                $("#actionMsg").html(str);
              });
            } else {
              $("#echartWrap").text(pageConstant.getDataErrorMessage);
            }
          }
        });
      }, 500);
    });

    //能力分布-散点图
    $("#vdCapacityPro").on("click", function() {
      $("#chartsModal").modal("show");
      pageConstant.removeContent("echartWrap", "actionMsg");  //清空绘制容器

      setTimeout(function() {
        var mdList = chartsCommon.getMdList(pageConstant.$itemObjList),
            scatter = Scatters("echartWrap");

        $.ajax({
          url: "/mining/capacity",
          type: "post",
          data: {
            "md_ids": JSON.stringify(mdList)
          },
          success: function(response) {
            var data = chartsCommon.getProportionPointData(response.result);
            scatter.makeScatter(data);
          }
        });
      }, 500);
    });

    //工作经历-散点图
    $("#vdCapacity").on("click", function() {
      $("#chartsModal").modal("show");
      pageConstant.removeContent("echartWrap", "actionMsg");  //清空绘制容器

      setTimeout(function() {
        var mdList = chartsCommon.getMdList(pageConstant.$itemObjList),
            scatter = Scatters("echartWrap");

        $.ajax({
          url: "/mining/capacity",
          type: "post",
          data: {
            "md_ids": JSON.stringify(mdList)
          },
          success: function(response) {
            var dataArr = chartsCommon.getPointDataList(response.result);
            scatter.makeScatter(dataArr);
          }
        });
      }, 500);
    });
  });
