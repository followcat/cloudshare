require.config({
  baseUrl: "/static/",
  paths: {
    'jquery': 'lib/js/jquery',
    'bootstrap': 'lib/js/bootstrap',
    'bootstraptable': 'lib/js/bootstrap-table.min',
    'header': 'src/js/util/header',
    'formvalidate': 'src/js/util/formvalidate',
    'Upload': 'src/js/util/upload',
    'radarcharts': 'src/js/util/charts/radarcharts',
    'barcharts': 'src/js/util/charts/barcharts',
    'scatters': "src/js/util/charts/scattercharts",
    'colorgrad': 'src/js/util/colorgrad',
    'History': 'src/js/util/history'
  },
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    }
  }
});
require(
  [
    'jquery',
    'radarcharts',
    'barcharts',
    'scatters',
    'colorgrad',
    'History',
    'bootstrap',
    'header',
    'formvalidate',
    'Upload',
    'bootstraptable'
  ],
  function($, radarcharts, barcharts, scattercharts, ColorGrad, History) {
    //Echarts - visualized data
    function isExist(array, value) {
      for (var i = 0, len = array.length; i < len; i++) {
        if (array[i].name === value) {
          return i;
        }
      }
      return false;
    }

    //Get the md_ids lists
    function GetMdLists() {
      var mdList = [];
      var titleList = $('.item-title');
      $.each(titleList, function(index, data) {
        var mdId = $(data).attr('href').split('/')[2];
        mdList.push(mdId);
      });

      return mdList;
    }

    //Echarts - visualized data

    //According to company for position
    function compare(value1, value2) {
      if (value1 > value2) {
        return 1;
      } else if (value1 < value2) {
        return -1;
      } else {
        return 0;
      }
    }

    //Deal with position data in mycharts
    function dealPosition(result) {
      var dataObj = {};
      $.each(result, function(index, data) {
        if (index !== $('input[name="search_text"]').val()) {
          if (data.length !== 1) {
            dataObj[index] = this;
          }
        }
      });
      return dataObj;
    }

    //button handle
    $('#vd-position').on('click', function() {
      //Ajax get data
      if ($('#data-main').css('display') === 'none') {
        $('#data-main').css('display', 'block');
        var barchart = barcharts('echarts-wrap');
        var formdata = {};
        //check search textarea element exist
        if ($('#search_textarea').length > 0) {
          formdata.search_text = '公司';
          formdata.md_ids = JSON.stringify(GetMdLists());
        } else {
          formdata.search_text = $('#search_text').val();
        }
        $.ajax({
          url: '/mining/position',
          type: 'post',
          data: { "search_text": $('#search_text').val()},
          success: function(response) {
            if (response.result !== '') {
              var dataArr = dealPosition(response.result);
              barchart.makeBar(dataArr);
              barchart.charts.on('click', function(params) {
                $('#action-msg').html('');
                var name = params.name,
                    str = '';
                for (var index in dataArr) {
                  if (name === index) {
                    str += '与<b>' + name + '</b>相关的人选:';
                    for (var i = 0, len = dataArr[index].length; i < len; i++) {
                      var link;
                      for (var filename in dataArr[index][i]) {
                        if (dataArr[index][i][filename].name !== '') {
                          str += "<a href='\/show\/" + filename + "' target='_blank'>" + dataArr[index][i][filename].name + "</a>";
                        } else {
                          str += "<a href='\/show\/" + filename + "' target='_blank'>-[" + filename + "]</a>";
                        }
                      }
                    }
                  }
                }
                $('#action-msg').html(str);
              });
            } else { /*if result end*/
              $('#data-main').text('无法获取到数据......');
            }
          }
        });
      } else {
        $('#data-main').css('display', 'none');
        $('#action-msg').text('');
      }
    });

    //return array
    function getCapacityDataArr(xData, yData) {
      var arr = [];
      arr[0] = xData;
      arr[1] = yData;
      return arr;
    }

    function getCapacityData(result) {
      var dataArr = new Array();
      for (var i = result.length - 1; i >= 0; i--) {
        var actpoint = 0,
            doclen = 0;
        var objArr = result[i];
        $.each(objArr, function(index, data) {
          actpoint += data.actpoint;
          doclen += data.doclen;
        });
        var actDoc = getCapacityDataArr(doclen, actpoint);
        dataArr.push(actDoc);
      }
      return dataArr;
    }

    //get Proportion point data
    function getProPointData(result) {
      var dataArr = new Array();
      for (var i = result.length - 1; i >= 0; i--) {
        var dataObj = {},
            personObj = result[i],
            capacity = personObj.capacity,
            scatterData = getScatterData(capacity),
            pro = (scatterData.actpointSum / scatterData.doclenSum) * 100,
            actdocPro = Math.pow(pro, 3);

        dataObj.fileName = personObj.md;
        dataObj.data = getCapacityDataArr(scatterData.workTime, pro);
        dataArr.push(dataObj);
        dataObj = null;
      }
      return dataArr;
    }

    //Echarts visualize data
    //能力分布
    $('#vd-capacity-pro').on('click', function() {
      $('#action-msg').html('');
      if ($('#data-main').css('display') === 'none') {
        $('#data-main').css('display', 'block');
        var mdList = GetMdLists();
        var scatter = scattercharts('echarts-wrap');

        $.ajax({
          url: '/mining/capacity',
          type: 'post',
          data: {
            'md_ids': JSON.stringify(mdList)
          },
          success: function(response) {
            var data = getProPointData(response.result);
            scatter.makeScatter(data);
          }
        });
      } else {
        $('#data-main').css('display', 'none');
      }
    });



    function changeTwoDecimal(x) {
      var f_x = parseFloat(x);
      f_x = Math.round(x * 100) / 100;

      var s_x = f_x.toString(),
          pos_decimal = s_x.indexOf('.');

      if (pos_decimal < 0) {
        pos_decimal = s_x.length;
        s_x += '.';
      }
      while (s_x.length <= pos_decimal + 2) {
        s_x += '0';
      }
      return s_x;
    }

    //get sum Month function
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

    //get working time function
    function getWorkTime(time) {
      var workingYear = parseInt(time / 12),
          workingMonth = time % 12,
          workingTime = changeTwoDecimal(workingYear + (workingMonth / 100));
      return workingTime;
    }

    //get scatter data array
    function getScatterData(capacity) {
      var time = 0,
          actpointSum = 0,
          doclenSum = 0;

      for (var i = capacity.length - 1; i >= 0; i--) {
        var obj = capacity[i];
        if (obj.begin !== '' && obj.end !== '') {
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
      // var actdocPro = (actpointSum/doclenSum) * 100;
      if (workTime < 40) {
        // return getCapacityDataArr(workTime, actdocPro);
        return {
          workTime: workTime,
          actpointSum: actpointSum,
          doclenSum: doclenSum
        };
      } else {
        return 0;
      }
    }

    function getPointData(result) {
      var dataArr = [];

      for (var i = result.length - 1; i >= 0; i--) {
        var dataObj = {},
            personObj = result[i];
        var capacity = personObj.capacity,
            scatterData = getScatterData(capacity);

        dataObj.fileName = personObj.md;
        dataObj.data = getCapacityDataArr(scatterData.workTime, scatterData.actpointSum);
        dataArr.push(dataObj);
        dataObj = null;
      }
      return dataArr;
    }

    //Echarts visualize data
    $('#vd-capacity').on('click', function() {
      $('#action-msg').html('');
      if ($('#data-main').css('display') === 'none') {
        $('#data-main').css('display', 'block');

        var scatter = scattercharts('echarts-wrap');
        var mdList = GetMdLists();

        $.ajax({
          url: '/mining/capacity',
          type: 'post',
          data: {
            'md_ids': JSON.stringify(mdList)
          },
          success: function(response) {
            var dataArr = getPointData(response.result);
            scatter.makeScatter(dataArr);
          }
        });
      } else {
        $('#data-main').css('display', 'none');
      }
    });

    //deal with something information
    var infoDeal = {};

    //if name is null, add name...
    infoDeal.NameAdd = function() {
      $(".name").each(function() {
        var aName = $(this);
        var nameBox = aName.find("span");
        var name_text = nameBox.text();

        if (name_text === "") {
          var title = aName.parent().parent().prev().find("a").text();
          var name = title.split("-")[0];
          nameBox.text(name);
        }
      });
    };

    infoDeal.NameAdd();
    //if age is "[]", delete the string of "[]"...
    infoDeal.DeleteSqBK = function() {
      $(".age").each(function() {
        var aAge = $(this);
        var ageBox = aAge.find("span");
        var age_text = ageBox.text();

        if (age_text === "[]") {
          ageBox.text("");
        }
      });
    };
    infoDeal.DeleteSqBK();

    function Toggle(obj) {
      obj.click(function() {
        var This = $(this);
        var aBlock = This.next();

        if (This.children().text() == "+") {
          This.children().text("-");
          aBlock.show();
          obj.flag = true;
        } else {
          This.children().text("+");
          aBlock.hide();
          This.flag = false;
        }
      });
    }

    var aLabelToggle = $(".label-alink");
    Toggle(aLabelToggle);

    var aCommentToggle = $(".comment-alink");
    Toggle(aCommentToggle);

    function AddedInfoHandler(obj) {
      var nextBro = obj.next();
      if (nextBro.css("display") === "none") {
        obj.children("span").text("-");
        nextBro.show();
      } else {
        obj.children("span").text("+");
        nextBro.hide();
      }
    }

    //tracking-link click event
    $(".tracking-link").on('click', function() {
        AddedInfoHandler($(this));
    });

    //comment-link click event
    $(".comment-link").on('click', function() {
        AddedInfoHandler($(this));
    });

    //show more experience
    $('.show-more').on('click', function() {
      var text = $(this).text();
      if (text.indexOf('Unfold') !== -1) {
        $(this).parent().find('.experience-hide').css({'display': 'block'});
        $(this).text('Fold');
      } else {
        $(this).parent().find('.experience-hide').css({'display': 'none'});
        $(this).text('Unfold');
      }
    });

    //匿名处理
    function replaceName(datas){
      for( var i = 0, datasLen = datas.length; i < datasLen; i++){
        for ( var j = 0, valuesLen = datas[i]['value'].length; j < valuesLen; j++){
          var name = datas[i]['value'][j]['name'];
          name = name.split('');
          if ( name.length === 2) {
            name[1] = '*';
          }else if ( name.length === 3 ) {
            name[1] = '*';
            name[2] = '*';
          }else if ( name.length === 4) {
            name[1] = '*';
            name[2] = '*';
            name[3] = '*';
          }else if ( name.length > 4){
            var temp = name;
            for (var z = temp.length - 1; z >= 3; z--) {
              temp[z] = '';
            }
            name = temp;
            name[1] = '*';
            name[2] = '*';
          }
          name = name.join('');
          datas[i]['value'][j]['name'] = name;
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
        var mdList = GetMdLists(),
            scatter = scattercharts('echarts-wrap');
        $.ajax({
          url: '/mining/capacity',
          type: 'post',
          data: {
            'md_ids': JSON.stringify(mdList)
          },
          success: function(response) {
            var data = getProPointData(response.result);
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
        var scatter = scattercharts('echarts-wrap');
        var mdList = GetMdLists();
        $.ajax({
          url: '/mining/capacity',
          type: 'post',
          data: {
            'md_ids': JSON.stringify(mdList)
          },
          success: function(response) {
            var dataArr = getPointData(response.result);
            scatter.makeScatter(dataArr);
          }
        });
      }, 500);
    });

    //根据选择的候选人绘制雷达图
    $('#vd-valuable').on('click', function() {
      $("#chartsModal").modal("show");
      removeContent();  //清空绘制容器
      var nameLists = getFileNameList($(".sel-item-name"));

      //定时器，等待modal渲染
      setTimeout(function(){
        var radar = radarcharts('echarts-wrap'),
            jdId = window.location.href.split(/(jd_id)=([\w]+)/)[2],
            reqData = null;
        if ( jdId ) {
          reqData = {
            'jd_id': jdId,
            'name_list': JSON.stringify(nameLists)
          };
        } else {
          var jdDoc = window.location.href.split(/(jd_doc)=/)[2];
          jdDoc = decodeURIComponent(jdDoc);
          reqData = {
            'jd_doc': jdDoc,
            'name_list': JSON.stringify(nameLists)
          };
        }
        $.ajax({
          url: '/analysis/valuable',
          type: 'post',
          data: reqData,
          success: function(response) {
            var datas;
            if ($('#anonymous-checkbox').is(':checked')){
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
    var itemLink = $('.item-link');
    var colorgrad = ColorGrad();  //创建渐变颜色实例
    for(var i = 0, len = itemLink.length; i < len; i++){
      var match = $(itemLink[i]).children('p').text();
      if (match === ''){
          break;
      }

      var matchToNum = parseFloat(match);
      var grad = colorgrad.gradient(parseInt(matchToNum*100));
      $(itemLink[i]).children('a').css({'color': grad});
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


    //控制抓取的数据的显示状态
    function crawlItemShow(val) {
      if ( val === "Liepin" ) {
        $(".crawl-item").css("display", "block");
      } else {
        $(".crawl-item").css("display", "none");
      }
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
          } else {
            if ( val === "Liepin" ) {
              $(".crawl-item").css("display", "none");
            }
          }
        }
      } else {
        databaseList = [];
        for ( var i = 0, len = $(".database-item").length; i < len; i++) {
          var ele = $(".database-item")[i];
          var val = $(ele).val();
          $(ele).attr("checked", "true");
          $(".crawl-item").css("display", "block");
        }
      }
    }
    initDatabase();

    //简历数据库选择
    $(".database-item").on("change", function(){
      var databaseList = null,
          lsDatabaseList = localStorage.databaseList;
      if ( lsDatabaseList ) {
        databaseList = JSON.parse(lsDatabaseList);
      } else {
        databaseList = [];
      }
      if ( $(this).is(":checked") ) {
        var val = $(this).val();
        databaseList.push(val);
      } else {
        databaseList.splice(databaseList.indexOf($(this).val()), 1);
      }
      crawlItemShow(val);
      localStorage.databaseList = JSON.stringify(databaseList);
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
      $(eleId).on('check.bs.table', function (e, row) {  //checked 事件监听
        var selName = row.name,
            selFileName = row.fileName;
        $("#sel-list").append("<div class=\"sel-item\">" +
          "<span class=\"sel-item-name\" data-filename=\""+ selFileName +"\">" + selName + "</span>" +
          "<span class=\"glyphicon glyphicon-remove sel-item-remove\" aria-hidden=\"true\"></span> </div>");
      })
      .on('uncheck.bs.table', function (e, row) {  //unchecked 事件监听
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
