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
    'use strict'

    /*
      @function: url参数截取
      @params: string
      @return: object
    */
    function queryString(str) {
      var arr = [],
          paramStr = "",
          jsonObj = {};
      if (str.indexOf("?") > 0) {
        paramStr = str.slice(str.indexOf("?")+1);
      }
      if (paramStr.indexOf("&") > 0) {
        arr = paramStr.split("&");
        for (var i = 0, len = arr.length; i < len; i++) {
          jsonObj[arr[i].split("=")[0]] = arr[i].split("=")[1];
        }
      } else {
        jsonObj[paramStr.split("=")[0]] = paramStr.split("=")[1];
      }
      return jsonObj;
    }

    var chartsCommon = new ChartsCommon();

    var m  = {
      currentURL: window.location.href,
      requestParam: queryString(window.location.href),
      conditions: ['currentPlaces', 'education', 'expectationPlaces', 'gender', 'marriedStatus'],
      /*
        @function: 匿名处理
        @params: array
        @return: array
      */
      replaceName: function(datas) {
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
      },
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
      },
      /*
        @function: 获取选择列表中的item
        @params: object
        @return: array
      */
      getSelectedFileNameList: function($oSelected) {
        var nameList = [];
        $oSelected.each(function() {
          nameList.push($(this).attr("data-filename"));
        });
        return nameList;
      }
    };

    //侧边栏 能力分布 按钮事件，显示图表
    $("#competencyBtn").on("click", function() {
      $("#chartsModal").modal("show");
      m.removeContent("echartWrap", "actionMsg");  //清空绘制容器

      //定时器，等待modal渲染
      setTimeout(function(){
        var mdList = chartsCommon.getMdList($(".item-title")),
            scatter = scattercharts("echartWrap");
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
    $("#experienceBtn").on("click", function(){
      $("#chartsModal").modal("show");
      m.removeContent("echartWrap", "actionMsg");  //清空绘制容器

      setTimeout(function(){
        var scatter = scattercharts("echartWrap");
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
    $("#vdValuable").on("click", function() {
      $("#chartsModal").modal("show");
      m.removeContent("echartWrap", "actionMsg");  //清空绘制容器
      var nameLists = m.getSelectedFileNameList($(".sel-item-name")),
          $databaseObj = $(".database-item"),
          uses = [];
      for (var i = $databaseObj.length; i >= 0; i--) {
        if ($($databaseObj[i]).is(":checked")) {
          uses.push($($databaseObj[i]).val());
        }
      }

      //定时器，等待modal渲染
      setTimeout(function(){
        var radar = radarcharts("echartWrap"),
            reqData = {};
        if ( m.requestParam.jd_id ) {
          reqData.jd_id = m.requestParam.jd_id;
        } else {
          reqData.jd_doc = decodeURIComponent(m.requestParam.jd_doc);
        }
        reqData.name_list = JSON.stringify(nameLists);
        reqData.uses = JSON.stringify(uses);

        $.ajax({
          url: "/analysis/valuable",
          type: "post",
          data: reqData,
          success: function(response) {
            var datas;
            if ($("#anonymous-checkbox").is(":checked")){
              datas = m.replaceName(response.data);
            }else{
              datas = response.data;
            }
            radar.makeRadar(datas, response.max);
          }
        });
      }, 500);
    });

    //根据匹配值大小描绘不同强度颜色
    var itemLink = $(".item-title");
    var colorgrad = ColorGrad();  //创建渐变颜色实例
    for(var i = 0, len = itemLink.length; i < len; i++){
      var match = $(itemLink[i]).attr("data-match");
      if (match === ""){
          break;
      }

      var matchToNum = parseFloat(match);
      var grad = colorgrad.gradient(parseInt(matchToNum*100));
      $(itemLink[i]).css({"color": grad});
    }

    //将item名字和对应的文件名加入localStorage中
    function addStorage(seletedObject){
      var nameLists = localStorage.nameLists ? JSON.parse(localStorage.nameLists) : [];
      nameLists.push(seletedObject);
      localStorage.setItem("nameLists", JSON.stringify(nameLists));
    }

    //将item名字和对应的文件名从localStorage中删除
    function deleteStorage(id, jd){
      var nameLists = localStorage.getItem("nameLists") ? JSON.parse(localStorage.getItem("nameLists")) : [];
      nameLists.forEach(function(obj, index) {
        if (obj.id === id && obj.jd === jd) {
          nameLists.splice(index, 1);  //remove
          localStorage.nameLists = JSON.stringify(nameLists);  //replace locaolStorage
        }
      });
    }

    //Checkbox勾选加入侧边栏中的选择列表
    $(".checkbox-name").on("click", function() {
      var nameLink = $(this).next();
      var $name = $(nameLink).text().split("-")[0],
          $mdFileName = $(nameLink).attr("href").split("/")[2],
          $id = $(nameLink).attr("data-id"),
          jd = m.requestParam.jd_id ? m.requestParam.jd_id : m.requestParam.jd_doc,
          seletedName = $name !== "" ? $name : $id;

      if ($(this).is(":checked")) {  //如果勾选，加入侧边栏
        $("#seletedList").append("<div class=\"sel-item\">" +
          "<span class=\"sel-item-name\" data-filename=\"" + $mdFileName +"\" data-id=\"" + $id + "\">" + seletedName + "</span>" +
          "<span class=\"glyphicon glyphicon-remove sel-item-remove\" aria-hidden=\"true\"></span> </div>");
        addStorage({
          name: seletedName,
          mdFileName: $mdFileName,
          id: $id,
          jd: jd
        });
      } else {  //取消勾选，从侧边栏删除
        var selItem = $(".sel-item-name");
        for (var i = 0, len = selItem.length; i < len; i++) {
          var self = $(selItem[i]);
          if ($id === self.attr("data-id")) {
            self.parent().remove();
            deleteStorage($id, jd);  //同时删除localStorage中对应的数据
          }
        }
      }
    });

    //选择列表中的item删除事件
    $("#seletedList").on("click", ".sel-item-remove", function() {
      var targetElement = $(this).prev();
      var $name = targetElement.text(),
          $mdFileName = targetElement.attr("data-filename"),
          $id = targetElement.attr("data-id"),
          jd = m.requestParam.jd_id ? m.requestParam.jd_id : m.requestParam.jd_doc;
      deleteStorage($id, jd);
      var itemTitle = $(".item-title");
      for ( var i = 0, len = itemTitle.length; i < len; i++) {
        var self = $(itemTitle[i]);
        if ( self.attr("data-id") === $id ) {
          self.prev().removeAttr("checked");
        }
      }
      $(this).parent().remove();
    });

    //从localStorage读取nameLists
    function readNameLists(){
      var nameLists = localStorage.nameLists ? JSON.parse(localStorage.nameLists) : [],
          jd = m.requestParam.jd_id ? m.requestParam.jd_id : m.requestParam.jd_doc;

      if (nameLists.length > 0) {
        nameLists.forEach(function(obj) {
          if (obj.jd === jd) {
            $("#seletedList").append("<div class=\"sel-item\">" +
              "<span class=\"sel-item-name\" data-filename=\"" + obj.mdFileName +"\" data-id=\"" + obj.id + "\">" + obj.name + "</span>" +
              "<span class=\"glyphicon glyphicon-remove sel-item-remove\" aria-hidden=\"true\"></span> </div>");
          }
        });
      }
    }
    readNameLists();

    //侧边栏按钮
    $("#operateMenu").on("click", function() {
      var $sideWidth = $(".sidebar-wrap").width(),
          $operateWidth = $("#operateMenu").width(),
          $sideRight = $(".sidebar-wrap").css("right");
      var moveLength = parseInt($sideWidth) - parseInt($operateWidth);
      //侧边栏动画
      if ( parseInt($sideRight) < 0){
        $(".sidebar-wrap").animate({right: "0"});
      } else {
        $(".sidebar-wrap").animate({right: "-" + moveLength.toString() + "px"});
      }
    });

    //页面加载初始化
    //根据侧边栏选择结果，修改item的checkbox状态
    function initCheckStatus(){
      var $selItem = $(".sel-item-name");
      if ( $selItem.length > 0 ) {
        var $resultItemTitle = $(".item-title");
        for ( var i = 0, len = $resultItemTitle.length; i < len; i++ ) {
          var self = $($resultItemTitle[i]);
          for ( var j = 0, selItemLen = $selItem.length; j < selItemLen; j++ ) {
            var $selectedId = $($selItem[j]).attr("data-id");
            if (self.attr("data-id") === $selectedId) {
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
        var selectedId = row.id,
            selectedName = row.name !== "" ? row.name : selectedId,
            selectedFileName = row.filename;

        $("#seletedList").append("<div class=\"sel-item\">" +
          "<span class=\"sel-item-name\" data-filename=\"" + selectedFileName +"\" data-id=\"" + selectedId + "\">" + selectedName + "</span>" +
          "<span class=\"glyphicon glyphicon-remove sel-item-remove\" aria-hidden=\"true\"></span> </div>");
      })
      .on("uncheck.bs.table", function (e, row) {  //unchecked 事件监听
          var $selItemLists = $(".sel-item-name");
          for (var i = 0, len = $selItemLists.length; i < len; i++) {
            var self = $($selItemLists[i]);
            if (row.id === self.attr("data-id")) {
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
        $("#historyModalBody").html("");  //清除更新前的表格
        $("#historyModalBody").append("<table id=\"historyTable\" data-show-refresh=\"true\" " +
          "data-click-to-select=\"true\" data-pagination=\"true\" data-search=\"true\" data-height=\"400\">" +
          "<thead>" +
            "<tr>" +
              "<th data-field=\"state\" data-checkbox=\"true\"></th>" +
              "<th data-field=\"id\">Id</th>" +
              "<th data-field=\"name\">Name</th>" +
              "<th data-field=\"filename\">File Name</th>" +
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

    //初始化数据库选择
    function initDatabase(){
      var databaseList = localStorage.databaseList ? JSON.parse(localStorage.databaseList) : [];

      for ( var i = 0, len = $(".database-item").length; i < len; i++) {
        var ele = $(".database-item")[i];
        var val = $(ele).val();
        if ( databaseList.indexOf(val) !== -1 ) {
          $(ele).attr("checked", "true");
        }
      }
    }
    initDatabase();

    //datalist保存至localstorage
    function saveInLocalStorage(checkedObj) {
      var databaseList = localStorage.databaseList ? JSON.parse(localStorage.databaseList) : [];

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
          paramObj = {},
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
        if (m.requestParam.jd_id) {
          newParams.jd_id = m.requestParam.jd_id;
        } else {
          newParams.jd_doc = m.requestParam.jd_doc;
        }
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
      var databaseList = saveInLocalStorage(checkedObj);

      var newParams = {},
          newUrl = "";
      if (m.requestParam.jd_id) {
        newParams.jd_id = m.requestParam.jd_id;
      } else {
        newParams.jd_doc = m.requestParam.jd_doc;
      }
      if (m.requestParam.page) {
        newParams.page = m.requestParam.page;
      } else {
        newParams.page = "1";
      }

      newParams.uses = databaseList;

      newUrl = "/lsipage?" + $.param(newParams);
      changePaginationUrl();
      window.location.href = newUrl;
    });

    /*
      条件过滤按钮点击事件
    */
    $("#filterBtn").on("click", function() {
      var str = "",
          databaseList = localStorage.databaseList ? JSON.parse(localStorage.databaseList) : [];
      if ( m.requestParam.jd_id ) {
        str = "<input type=\"text\" name=\"jd_id\" value=\""+ m.requestParam.jd_id +"\" style=\"display: none\">";
      } else {
        str  = "<input type=\"text\" name=\"jd_id\" value=\""+ decodeURIComponent(m.requestParam.jd_doc) +"\" style=\"display: none\">";
      }
      $("#filterForm").append(str);
      str = "<input type=\"text\" name=\"uses\" value=\""+ JSON.stringify(databaseList).replace(/"/g, "\'") +"\" style=\"display: none\">";
      $("#filterForm").append(str);
      $("#filterForm").submit();
    });

    //过滤条件
    function setFilterCondition(elementId) {
      elementId = '#' + elementId;
      var conditionStr = "";
      for (var i = m.conditions.length; i >= 0; i--) {
        conditionStr = m.requestParam[m.conditions[i]] ? m.requestParam[m.conditions[i]] : "";
        if (conditionStr !== "") {
          $(elementId).append(decodeURIComponent(conditionStr) + ' ');
        } else {
          $(elementId).append(decodeURIComponent(conditionStr));
        }
      }
    }
    setFilterCondition("conditionList");

  });
