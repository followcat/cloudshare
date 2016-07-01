require.config({
  baseUrl: "/static/",
  paths: {
    "jquery": "lib/js/jquery",
    "bootstrap": "lib/js/bootstrap",
    "bootstraptable": "lib/js/bootstrap-table.min",
    "header": "src/js/util/header",
    "formvalidate": "src/js/util/formvalidate",
    "Upload": "src/js/util/upload",
    "radarcharts": "src/js/util/charts/radarcharts",
    "barcharts": "src/js/util/charts/barcharts",
    "scatters": "src/js/util/charts/scattercharts",
    "colorgrad": "src/js/util/colorgrad",
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
    "radarcharts",
    "barcharts",
    "scatters",
    "colorgrad",
    "History",
    "ChartsCommon",
    "bootstrap",
    "header",
    "formvalidate",
    "Upload",
    "bootstraptable",
    "ProcessInfo"
  ],
  function($, radarcharts, barcharts, scattercharts, ColorGrad, History, ChartsCommon) {
    var chartsCommon = new ChartsCommon();
    //匿名处理
    function replaceName(datas){
      for( var i = 0, datasLen = datas.length; i < datasLen; i++){
        for ( var j = 0, valuesLen = datas[i]["value"].length; j < valuesLen; j++){
          var name = datas[i]["value"][j]["name"];
          name = name.split("");
          if ( name.length === 2) {
            name[1] = "*";
          }else if ( name.length === 3 ) {
            name[1] = "*";
            name[2] = "*";
          }else if ( name.length === 4) {
            name[1] = "*";
            name[2] = "*";
            name[3] = "*";
          }else if ( name.length > 4){
            var temp = name;
            for (var z = temp.length - 1; z >= 3; z--) {
              temp[z] = "";
            }
            name = temp;
            name[1] = "*";
            name[2] = "*";
          }
          name = name.join("");
          datas[i]["value"][j]["name"] = name;
        }
      }
      return datas;
    }

    //清空图表绘制容器的内容
    function removeContent(){
      $("#echarts-wrap").html("");
      $("#action-msg").html("");
    }

    //获取选择列表中item
    function getFileNameList(obj){
      var nameLists = [];
      obj.each(function(){
        nameLists.push($(this).attr("data-filename"));
      });
      return nameLists;
    }

    //侧边栏 能力分布 按钮事件，显示图表
    $("#competency-btn").on("click", function() {
      $("#chartsModal").modal("show");
      removeContent();  //清空绘制容器

      //定时器，等待modal渲染
      setTimeout(function(){
        var mdList = chartsCommon.getMdList($(".item-title")),
            scatter = scattercharts("echarts-wrap");
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

    //侧边栏 经验分布 按钮事件，显示图表
    $("#experience-btn").on("click", function(){
      $("#chartsModal").modal("show");
      removeContent();  //清空绘制容器

      setTimeout(function(){
        var scatter = scattercharts("echarts-wrap");
        var mdList = chartsCommon.getMdList($(".item-title"));
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

    //根据选择的候选人绘制雷达图
    $("#vd-valuable").on("click", function() {
      $("#chartsModal").modal("show");
      removeContent();  //清空绘制容器
      var nameLists = getFileNameList($(".sel-item-name"));

      //定时器，等待modal渲染
      setTimeout(function(){
        var radar = radarcharts("echarts-wrap"),
            jdId = window.location.href.split(/(jd_id)=([\w]+)/)[2],
            reqData = null;
        if ( jdId ) {
          reqData = {
            "jd_id": jdId,
            "name_list": JSON.stringify(nameLists)
          };
        } else {
          var jdDoc = window.location.href.split(/(jd_doc)=/)[2];
          jdDoc = decodeURIComponent(jdDoc);
          reqData = {
            "jd_doc": jdDoc,
            "name_list": JSON.stringify(nameLists)
          };
        }
        $.ajax({
          url: "/analysis/valuable",
          type: "post",
          data: reqData,
          success: function(response) {
            var datas;
            if ($("#anonymous-checkbox").is(":checked")){
              datas = replaceName(response.data);
            }else{
              datas = response.data;
            }
            radar.makeRadar(datas, response.max);
          }
        });
      }, 500);
    });

    //根据匹配值大小描绘不同强度颜色
    var itemLink = $(".item-link");
    var colorgrad = ColorGrad();  //创建渐变颜色实例
    for(var i = 0, len = itemLink.length; i < len; i++){
      var match = $(itemLink[i]).children("p").text();
      if (match === ""){
          break;
      }

      var matchToNum = parseFloat(match);
      var grad = colorgrad.gradient(parseInt(matchToNum*100));
      $(itemLink[i]).children("a").css({"color": grad});
    }

    //将item名字和对应的文件名加入localStorage中
    function addStorage(name, mdFileName, flag){
      var nameLists = null,
          lsNameLists = localStorage.nameLists;
      if ( lsNameLists ) {
        nameLists = JSON.parse(lsNameLists);
      } else {
        nameLists = new Array();
      }
      nameLists.push( { name: name, mdFileName: mdFileName, flag: flag });
      localStorage.setItem("nameLists", JSON.stringify(nameLists));
    }

    //将item名字和对应的文件名从localStorage中删除
    function deleteStorage(name, mdFileName, flag){
      var nameLists = JSON.parse(localStorage.getItem("nameLists"));
      nameLists.forEach(function(obj, index) {
        if ( obj.name === name && obj.mdFileName === mdFileName && obj.flag === flag ) {
          nameLists.splice(index, 1);  //remove
          localStorage.nameLists = JSON.stringify(nameLists);  //replace locaolStorage
        }
      });
    }

    //Checkbox勾选加入侧边栏中的选择列表
    $(".checkbox-name").on("click", function() {
      var nameLink = $(this).next();
      var name = $(nameLink).text().split("-")[0],
          mdFileName = $(nameLink).attr("href").split("/")[2],
          flag = window.location.href.split("=")[1];
      if ( $(this).is(":checked") ) {  //如果勾选，加入侧边栏
        $("#sel-list").append("<div class=\"sel-item\">" +
          "<span class=\"sel-item-name\" data-filename=\""+ mdFileName +"\">" + name + "</span>" +
          "<span class=\"glyphicon glyphicon-remove sel-item-remove\" aria-hidden=\"true\"></span> </div>");
          addStorage(name, mdFileName, flag);
      } else {  //取消勾选，从侧边栏删除
        var selItem = $(".sel-item-name");
        for ( var i = 0, len = selItem.length; i < len; i++) {
          var self = $(selItem[i]);
          if ( mdFileName === self.attr("data-filename") ) {
            self.parent().remove();
            deleteStorage(name, mdFileName, flag);  //同时删除localStorage中对应的数据
          }
        }
      }
    });

    //选择列表中的item删除事件
    $("#sel-list").on("click", ".sel-item-remove", function() {
      var name = $(this).prev().text(),
          mdFileName = $(this).prev().attr("data-filename"),
          flag = window.location.href.split("=")[1];
      deleteStorage(name, mdFileName, flag);
      var itemTitle = $(".item-title");
      for ( var i = 0, len = itemTitle.length; i < len; i++) {
        var self = $(itemTitle[i]);
        if ( self.text().indexOf(name) !== -1 ) {
          self.prev().removeAttr("checked");
        }
      }
      $(this).parent().remove();
    });

    //从localStorage读取nameLists
    function readNameLists(){
      if ( localStorage.nameLists ) {
        var nameLists = JSON.parse(localStorage.nameLists),
            flag = window.location.href.split("=")[1];
        if ( nameLists.length > 0 ) {
          nameLists.forEach( function( obj ) {
            if ( obj.flag === flag ) {
              $("#sel-list").append("<div class=\"sel-item\">" +
                "<span class=\"sel-item-name\" data-filename=\""+ obj.mdFileName +"\">" + obj.name + "</span>" +
                "<span class=\"glyphicon glyphicon-remove sel-item-remove\" aria-hidden=\"true\"></span> </div>");
            }
          });
        }
      }
    }
    readNameLists();

    //侧边栏按钮
    $("#operateMenu").on("click", function() {
      var sideWidth = $(".sidebar-wrap").width(),
          operateWidth = $("#operateMenu").width(),
          sideRight = $(".sidebar-wrap").css("right");
      var moveLength = parseInt(sideWidth) - parseInt(operateWidth);
      //侧边栏动画
      if ( parseInt(sideRight) < 0){
        $(".sidebar-wrap").animate({right: "0"});
      } else {
        $(".sidebar-wrap").animate({right: "-" + moveLength.toString() + "px"});
      }
    });

    //url参数截取，返回参数对象
    function queryString(str) {
      var arr = [],
          jsonObj = {};
      if (str.indexOf("?") > 0) {
        arr = str.slice(str.indexOf("?")+1);
      }
      if (arr.indexOf("&") > 0) {
        arr = str.slice(str.indexOf("?")+1).split("&");
        for (var i = 0, len = arr.length; i < len; i++) {
          jsonObj[arr[i].split("=")[0]] = arr[i].split("=")[1];
        }
      }
      return jsonObj;
    }

    //初始化数据库选择
    function initDatabase(){
      var databaseList = null,
          lsDatabaseList = localStorage.databaseList;
      if ( lsDatabaseList ) {
        databaseList = JSON.parse(lsDatabaseList);
        for ( var i = 0, len = $(".database-item").length; i < len; i++) {
          var ele = $(".database-item")[i];
          var val = $(ele).val();
          if ( databaseList.indexOf(val) !== -1 ) {
            $(ele).attr("checked", "true");
          }
        }
      }
    }
    initDatabase();

    //datalist保存至localstorage
    function saveInLocalStorage(checkedObj) {
      var databaseList = null,
          lsDatabaseList = localStorage.databaseList;
      if ( lsDatabaseList ) {
        databaseList = JSON.parse(lsDatabaseList);
      } else {
        databaseList = [];
      }
      if ( checkedObj.is(":checked") ) {
        databaseList.push(checkedObj.val());
      } else {
        databaseList.splice(databaseList.indexOf(checkedObj.val()), 1);
      }
      localStorage.databaseList = JSON.stringify(databaseList);
      return databaseList;
    }

    //修改分页url
    function changePaginationUrl() {
      var linkHref = "",
          paramObj = "",
          dbParam = [],
          databaseList = localStorage.databaseList;
      if (databaseList) {
        dbParam = JSON.parse(databaseList);
      } else {
        dbParam = null;
      }

      //遍历所有a标签
      $(".pagination a").map(function(){
        linkHref = $(this).attr("href");
        paramObj = queryString(linkHref);
        var newParams = {};
        newParams.jd_id = paramObj.jd_id;
        newParams.page = paramObj.page;
        newParams.uses = dbParam;
        var newUrl = "/lsipage?" + $.param(newParams);
        $(this).attr("href", newUrl);
      });
    }
    //加载完后直接调用
    changePaginationUrl();

    //简历数据库选择
    $(".database-item").on("change", function(){
      var checkedObj = $(this);
      var databaseList = saveInLocalStorage(checkedObj),
          paramObj = queryString(location.href);

      var newParams = {},
          newUrl = "";
      newParams.jd_id = paramObj.jd_id;
      newParams.page = paramObj.page;
      newParams.uses = databaseList;

      newUrl = "/lsipage?" + $.param(newParams);
      changePaginationUrl();
      window.location.href = newUrl;
    });


    //页面加载初始化
    //根据侧边栏选择结果，修改item的checkbox状态
    function initCheckStatus(){
      var selItem = $(".sel-item-name");
      if ( selItem.length > 0 ) {
        var resultItemTitle = $(".item-title");
        for ( var i = 0, len = resultItemTitle.length; i < len; i++ ) {
          var self = $(resultItemTitle[i]);
          for ( var j = 0, selItemLen = selItem.length; j < selItemLen; j++ ) {
            var selItemName = $(selItem[j]).text(),
                selItemMdFileName = $(selItem[j]).attr("data-filename");
            if ( self.text().indexOf(selItemName) !== -1 && self.attr("href").indexOf(selItemMdFileName) !== -1 ) {
              self.prev().attr("checked", true);
            }
          }
        }
      }
    }
    initCheckStatus();

    //历史记录选择事件绑定
    function bindHistorySelect(eleId) {
      $(eleId).on("check.bs.table", function (e, row) {  //checked 事件监听
        var selName = row.name,
            selFileName = row.fileName;
        $("#sel-list").append("<div class=\"sel-item\">" +
          "<span class=\"sel-item-name\" data-filename=\""+ selFileName +"\">" + selName + "</span>" +
          "<span class=\"glyphicon glyphicon-remove sel-item-remove\" aria-hidden=\"true\"></span> </div>");
      })
      .on("uncheck.bs.table", function (e, row) {  //unchecked 事件监听
          var selItemLists = $(".sel-item-name");
          for ( var i = 0, len = selItemLists.length; i < len; i++ ) {
            var self = $(selItemLists[i]);
            if ( row.name === self.text() && row.fileName === self.attr("data-filename") ) {
              self.parent().remove();
            }
          }
      });
    }

    //历史记录按钮事件
    //在模态框展示历史记录
    $("#hisBtnTrigger").on("click", function(){
      $("#historyModal").modal("show");
      var history = new History();
      var lists = history.readHistory();
      if ( $("#historyTable tbody").length === 0 ) {
        setTimeout(function(){
          $("#historyTable").bootstrapTable({
            data: lists.reverse()
          });
          bindHistorySelect("#historyTable");
        }, 500);
      } else {
        $("#historyModalBody").html("");  //清楚更新前的表格
        $("#historyModalBody").append("<table id=\"historyTable\" data-show-refresh=\"true\" " +
          "data-click-to-select=\"true\" data-pagination=\"true\" data-search=\"true\" data-height=\"400\">" +
          "<thead>" +
            "<tr>" +
              "<th data-field=\"state\" data-checkbox=\"true\"></th>" +
              "<th data-field=\"name\">Name</th>" +
              "<th data-field=\"fileName\">File Name</th>" +
              "<th data-field=\"time\">Time</th>" +
            "</tr>" +
          "</thead>" +
        "</table>");  //重新插入表结构
        setTimeout(function(){
          $("#historyTable").bootstrapTable({
            data: lists.reverse()
          });  //读取赋值
          bindHistorySelect("#historyTable");  //对新表格进行事件绑定
        }, 500);
      }
    });


  });
