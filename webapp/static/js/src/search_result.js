require.config({

	baseUrl: "../static/js",

	paths: {
		'jquery': 'lib/jquery',
		'bootstrap': 'lib/bootstrap',
		'header': 'src/header',
		'formvalidate': 'src/formvalidate',
		'Upload': 'src/upload',
		'echarts': 'lib/source'
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
		'echarts', 
		'echarts/theme/macarons', 
		'echarts/chart/line', 
		'echarts/chart/bar',
		'echarts/chart/map',
		'echarts/chart/scatter',
		'bootstrap', 
		'header', 
		'formvalidate', 
		'Upload',
	], function($, ec){


	//Echarts - visualized data

	function isExist(array, value){

		for(var i = 0, len = array.length; i < len; i++){

			if(array[i].name === value){

				return i;

			}
		}

		return false;
	}

	//Show position region on the map

	//Deal with Md lists and its region source

	function GetRegionList(resultArr){

		var regionDataArr = new Array();
		var geoObj = new Object();

		for(var i = 0, iLen = resultArr.length; i < iLen; i++){

			var subArr = resultArr[i];

			for(var j = 0, jLen = subArr.length; j < jLen; j++){

			  var obj = subArr[j];

			  //init regionDataArr 

			  if(obj.name){

				  if(regionDataArr.length === 0){

			 		 	var regionObj = new Object();

			 		 	regionObj.name = obj.name;

			 		 	regionObj.value = 1;

			 		 	geoObj[obj.name] = [obj.coord[0], obj.coord[1]];

			 		 	regionDataArr.push(regionObj);

			 		 	regionObj = null;

				  }else{

				  	var index = isExist(regionDataArr, obj.name);

				  	if(index || index === 0){

				  		regionDataArr[index].value += 1;

				  	}else{

				  		 var regionObj = new Object();

				 		 	regionObj.name = obj.name;

				 		 	regionObj.value = 1;

				 		 	geoObj[obj.name] = [obj.coord[0], obj.coord[1]];

				 		 	regionDataArr.push(regionObj);

				 		 	regionObj = null;	

				  	}
				  }
				}
			}
		}

		return {

			regionDataArr: regionDataArr,

			geoObj: geoObj

		}
	}


 //Get the md_ids lists

 function GetMdLists(){

 	 var mdList = [];

			var titleList = $('.item-title');

			$.each(titleList, function(index, data){

				var mdId = $(data).attr('href').split('/')[2];

				mdList.push(mdId);

			});

			return mdList;

 }


	//Show position region button handle

	$('#vd-position-region').on('click', function(){

		$('#action-msg').text('');

		if($('#data-main').css('display') === 'none'){

			$('#data-main').css('display', 'block');

			var positionCharts = ec.init(document.getElementById('echarts-wrap'), 'macarons');

			positionCharts.showLoading({

				text: '数据加载中...',

				effect: 'whirling',

				textStyle: {

					fontSize: 20

				}
			});

			//Get the md_ids lists

			var mdList = GetMdLists();

			$.ajax({

				url: '/mining/region',

				type: 'post',

				data: {
					'md_ids': JSON.stringify(mdList)
				},

				success: function(response){

					var regionObj = GetRegionList(response.result);

					positionCharts.hideLoading();

					var option = {

				    title : {
				        text: '职业分布情况',
				        x:'center'
				    },

				    tooltip : {
				        trigger: 'item'
				    },

				    dataRange: {
				        min : 0,
				        max : 500,
				        calculable : true,
				        color: ['#191970','#4D4D4D','#551A8B','#CD0000']
				    },

				    toolbox: {
				        show : true,
				        orient : 'vertical',
				        x: 'right',
				        y: 'center',
				        feature : {
				            mark : {show: true},
				            dataView : {show: true, readOnly: false},
				            restore : {show: true},
				            saveAsImage : {show: true}
				        }
				    },

				    series : [{
				      name: 'region',

				      type: 'map',

				      mapType: 'china',

				      hoverable: false,

				      roam:true,

          data : [],

				      markPoint : {
				        symbolSize: 10,       // 标注大小，半宽（半径）参数，当图形为方向或菱形则总宽度为symbolSize * 2

				        itemStyle: {

				          normal: {
				            borderColor: '#87cefa',
				            borderWidth: 1,            // 标注边线线宽，单位px，默认为1
				            label: {
				              show: true
				            }
				          },
				          emphasis: {

				            borderColor: '#1e90ff',

				            borderWidth: 5,

				            label: {
				              show: false
				            }
				          }
				        },

				        data : function(){
              var list = [];

              for (var i = regionObj.regionDataArr.length - 1; i >= 0; i--) {
              	 if(regionObj.regionDataArr[i].value > 2){
              	 	 list.push(regionObj.regionDataArr[i]);
              	 }else{
              	 	 continue;
              	 }
              }
              return list;

				        }()

				      },

				      geoCoord: regionObj.geoObj

				    }]
					};
                      /*end option*/

					positionCharts.setOption(option);

				}
			});
		}else{
			$('#data-main').css('display', 'none');
		}
	});

	//Echarts - visualized data

	//According to company for position

	function compare(value1, value2){
		if(value1 > value2){
			return 1;
		}else if(value1 < value2){
			return -1;
		}else{
			return 0;
		}
	}

	//Deal with position data in mycharts

	function dealPosition(result){
		
		var dataArr = new Array();

		$.each(result, function(index, data){

			if(index !== $('input[name="search_text"]').val()){

				if(data.length !== 1){

					var obj = new Object();

					obj.name = index;

					obj.value = data.length;

					obj.source = data;

					dataArr.push(obj);

					obj = null;

				}

			}

		});

		return dataArr;

	}

	//button handle
	$('#vd-position').on('click', function(){

		//Ajax get data

		if( $('#data-main').css('display') === 'none'){

			$('#data-main').css('display', 'block');

			var myCharts = ec.init(document.getElementById('echarts-wrap'), 'macarons');

			myCharts.showLoading({

				text: '数据加载中...',

				effect: 'whirling',

				textStyle: {

					fontSize: 20

				}

			});

   var search_text;

   //check search textarea element exist
   if($('#search_textarea').length > 0){
   
     search_text = '公司';
   
   }else{
     
     search_text = $('#search_text').val()

   }
   console.log(search_text);
			$.ajax({

				url: '/mining/position',

				type: 'get',

				data:{
					'search_text' : search_text
				},

				success: function(response){

					if(response.result !== ''){

			   var dataArr = dealPosition(response.result);

						myCharts.hideLoading();

						var option = {

							title: {
								text: '职位'
							},

							tooltip: {
								trigger: 'axis'
							},

							toolbox: {
								show: true,

								feature: {

									dataView: { show: true, readOnly: true },

									magicType : {show: true, type: ['line', 'bar']},

									restore: { show: true },

									saveAsImage: { show: true }

								}
							},

							xAxis: [
								{
									type: 'category',

									data: function(){

									  var list = [];

									  for(var i = 0, len = dataArr.length; i < len; i++){
                      
             list.push(dataArr[i].name);

									  }

									  return list;

									}(),

									axisLabel: {

										rotate: 20

									}
								}
							],

							yAxis: [
								{

									type: 'value'

								}
       ],

							series: [
							{
									name: '数量',
									type: 'bar',
									data: function(){
										
										var list = [];

          for(var i = 0, len = dataArr.length; i < len; i++){
                      
             list.push(dataArr[i].value);

           }

           return list;

									}()
								}
							]
						};

						myCharts.setOption(option);

						//Echarts event handle

 	    var ecConfig = require('echarts/config');
						
						myCharts.on(ecConfig.EVENT.CLICK, function(param){
              
        //init action massage box html
        $('#action-msg').html('');

        var name = param.name;
        
        var str = '';

        for(var i = 0, len = dataArr.length; i < len; i++){

        	if( name === dataArr[i].name ){

            var source = dataArr[i].source;

            str = '与<b>' + name + '</b>相关的人选:';

            $.each(source, function(index, data){
              
              var link;

              for(var obj in data){
              	 if(data[obj].name === ''){
              	 
              	   str += "<a href='\/show\/" + obj + "' target='_blank'>-[" + obj + "]</a>";
              	 
              	 }else{

                  str += "<a href='\/show\/" + obj + "' target='_blank'>" + data[obj].name + "</a>";
                
                }
              }
     
            });

        	}

        }
        
        $('#action-msg').html(str);

						});

					}else{/*if result end*/

						$('#data-main').text('无法获取到数据......');

					}         
				}
			});
			
		}else{

			$('#data-main').css('display', 'none');

   $('#action-msg').text('');

  }
		
	});

//return array

function getCapacityDataArr(xData, yData){
  
  var arr = [];

  arr[0] = xData;

  arr[1] = yData;

  return arr;
}

function getCapacityData(result){

  var dataArr = new Array();

  for (var i = result.length - 1; i >= 0; i--) {

    var actpoint = 0, 
        doclen = 0;

    var objArr = result[i];
    
    $.each(objArr, function(index, data){
    
      actpoint += data.actpoint;

      doclen += data.doclen;
      
    });

    var actDoc = getCapacityDataArr(doclen, actpoint);

    dataArr.push(actDoc);

  };

  return dataArr;

}

//get Proportion point data

function getProPointData(result){

  var dataArr = new Array();
  
  for (var i = result.length - 1; i >= 0; i--) {

    var dataObj = {};

    var personObj = result[i];
    
    var capacity = personObj.capacity;
    
    var scatterData = getScatterData(capacity);
    
    var pro = (scatterData.actpointSum / scatterData.doclenSum) * 100;
    var actdocPro = Math.pow(pro, 3);

    dataObj.fileName = personObj.md;

    dataObj.data = getCapacityDataArr(scatterData.workTime, pro);
    
    dataArr.push(dataObj);
    
    dataObj = null;

  }

  return dataArr;

}

//Echarts visualize data

$('#vd-capacity-pro').on('click', function(){

  $('#action-msg').html('');
  
  if($('#data-main').css('display') === 'none'){

    $('#data-main').css('display', 'block');

    var mdList = GetMdLists();
    
    var scatterCharts = ec.init(document.getElementById('echarts-wrap'), 'macarons');

    scatterCharts.showLoading({

      text: '数据加载中...',

      effect: 'whirling',

      textStyle: {

        fontSize: 20

      }

    });

    $.ajax({
    
     url: '/mining/capacity',

     type: 'post',

     data: {
       'md_ids': JSON.stringify(mdList)
     },

     success: function(response){

       var data = getProPointData(response.result);

       scatterCharts.hideLoading();

       var scatterOption = {
       
         title: {
           text: '能力分布'
         },
         
         tooltip: {
           trigger: 'axis',
           
           showDelay: 0,
           
           formatter: function(params){
             
             if(params.value.length > 1){
               
               return params.value[0] + '年' + params.value[1] + '个';

             }

           },

           axisPointer:{
            show: true,
            type : 'cross',
            lineStyle: {
                type : 'dashed',
                width : 1
            }
           }
         },

         toolbox: {
           show : true,
           feature : {
             mark : {show: true},
             dataZoom : {show: true},
             dataView : {show: true, readOnly: false},
             restore : {show: true},
             saveAsImage : {show: true}
           }
         },

         xAxis : [
         {
           type : 'value',
           scale:true,
           axisLabel: {
             formatter: '{value} 年'
           }
         }],

         yAxis : [
         {
           type : 'value',
           scale:true,
           axisLabel: {
             formatter: '{value} 个'
           }
         }],

         series : [
         {
           name: 'test',

           type: 'scatter',

           data: function(){

             var list = [];

             for(var i = 0, len = data.length; i < len; i++){

               list.push(data[i].data);

             }

             return list;

           }()

         }]
       
       };
      
        scatterCharts.setOption(scatterOption);
        
        var ecConfig = require('echarts/config');
 
        scatterCharts.on(ecConfig.EVENT.CLICK, function(param){

          var index = param.dataIndex;
          
          var a = $("<a href=\'\/show\/"+data[index].fileName+"\' target=\'_blank\'><\/a>").get(0);  
              
          var e = document.createEvent('MouseEvents');  

          e.initEvent('click', true, true);  
          a.dispatchEvent(e);
						  
        });

      }

    });
		}else{

			$('#data-main').css('display', 'none');

		}
});


function changeTwoDecimal(x) {

  var f_x = parseFloat(x);

  f_x = Math.round(x * 100) / 100;

  var s_x = f_x.toString();

  var pos_decimal = s_x.indexOf('.');

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

function getSumMonth(beginYear, beginMonth, endYear, endMonth){

  	var year = endYear - beginYear;
  	var month, 
  	    monthCount;
    
  	if( year < 0 ){

  		 return -1;
  	
  	}else{
          
     if( parseInt(beginMonth) < parseInt(endMonth) ){

  	    month = endMonth - beginMonth;
  	  
  	  }else{
  		   
  		   month = beginMonth - endMonth;
  	  
  	  }

     monthCount = year * 12 + month;
     
  	  return monthCount;

  	}
  	
}

//get working time function

function getWorkTime(time){

  var workingYear = parseInt(time / 12);
  
  var workingMonth = time % 12;

  var workingTime = changeTwoDecimal(workingYear + ( workingMonth / 100));

  return workingTime;

}

//get scatter data array

function getScatterData(capacity){
  
  var time = 0, actpointSum = 0, doclenSum = 0;

  for (var i = capacity.length - 1; i >= 0; i--) {
  	 
  	 var obj = capacity[i];
    
    if( obj.begin !== '' && obj.end !== '' ){
      
      var num = getSumMonth(obj.begin[0], obj.begin[1], obj.end[0], obj.end[1]);

      if( num === -1){
        continue;
      }else{

        time += num;

        actpointSum += obj.actpoint;

        doclenSum += obj.doclen;

      }
    }
  };

  var workTime = getWorkTime(time);

  // var actdocPro = (actpointSum/doclenSum) * 100;

  if ( workTime < 40 ){
    
    // return getCapacityDataArr(workTime, actdocPro);
    return { workTime: workTime, actpointSum: actpointSum, doclenSum: doclenSum };

  }else{

  	 return 0;

  }

}

function getPointData(result){

  var dataArr = new Array();
  
  for (var i = result.length - 1; i >= 0; i--) {

    var dataObj = {};

    var personObj = result[i];
    
    var capacity = personObj.capacity;
    
    var scatterData = getScatterData(capacity);
    
    dataObj.fileName = personObj.md;

    dataObj.data = getCapacityDataArr(scatterData.workTime, scatterData.actpointSum);

    dataArr.push(dataObj);

    dataObj = null;

  }

  return dataArr;

}

//Echarts visualize data

$('#vd-capacity').on('click', function(){

	 $('#action-msg').html('');
  
  if($('#data-main').css('display') === 'none'){

			 $('#data-main').css('display', 'block');
    
    var timeCharts = ec.init(document.getElementById('echarts-wrap'), 'macarons');

    timeCharts.showLoading({

				 text: '数据加载中...',

				 effect: 'whirling',

				 textStyle: {

					 fontSize: 20

				 }

				});

    var mdList = GetMdLists();

				$.ajax({

      url: '/mining/capacity',

      type: 'post',

      data: {
        'md_ids': JSON.stringify(mdList)
      },

      success: function(response){
        
        var dataArr = getPointData(response.result);

        timeCharts.hideLoading();

        var timeOption = {

          title: {
            text: '工作经验分布'
          },
         
          tooltip: {
            trigger: 'axis',
           
            showDelay: 0,
           
            formatter: function(params){
              
              if(params.value.length > 1){
               
                return params.value[0] + '年' + params.value[1] + '个' ;

              }

            },

	           axisPointer:{
	            show: true,
	            type : 'cross',
	            lineStyle: {
	                type : 'dashed',
	                width : 1
	            }
	           }
	         },

	         toolbox: {
	           show : true,
	           feature : {
	             mark : {show: true},
	             dataZoom : {show: true},
	             dataView : {show: true, readOnly: false},
	             restore : {show: true},
	             saveAsImage : {show: true}
	           }
	         },

	         xAxis : [
	         {
	           type : 'value',
	           scale:true,
	           axisLabel: {
	             formatter: '{value} 年'
	           }
	         }],

	         yAxis : [
	         {
	           type : 'value',
	           scale:true,
	           axisLabel: {
	             formatter: '{value} 个'
	           }
	         }],

	         series : [
	         {
	           name: '工作经验',

	           type: 'scatter',

	           data: function(){
	             var list = [];

	             for(var i = 0, len = dataArr.length; i < len; i++){

	               list.push(dataArr[i].data);

	             }

	             return list;
	           }()

	         }]
	       
	       };
        
        timeCharts.setOption(timeOption);

        var ecConfig = require('echarts/config');
						
						  timeCharts.on(ecConfig.EVENT.CLICK, function(param){

          var index = param.dataIndex;
          
          var a = $("<a href='\/show\/" + dataArr[index].fileName + "\' target='_blank'>click</a>").get(0);  
              
          var e = document.createEvent('MouseEvents');  

          e.initEvent('click', true, true);  
          a.dispatchEvent(e);

						  });

      }

				});

		}else{

			 $('#data-main').css('display', 'none');

		}
});

	//deal with something information
	var infoDeal = {};

	//if name is null, add name...
	infoDeal.NameAdd = function(){

		$(".name").each(function(){

			var aName = $(this);

			var nameBox = aName.find("span");

			var name_text = nameBox.text();

			if(name_text === ""){

				var title = aName.parent().parent().prev().find("a").text();

				var name = title.split("-")[0];

				nameBox.text(name);

			}
		});
	};

	infoDeal.NameAdd();
	
	//if age is "[]", delete the string of "[]"...

	infoDeal.DeleteSqBK = function(){

		$(".age").each(function(){

			var aAge = $(this);

			var ageBox = aAge.find("span");

			var age_text = ageBox.text();

			if(age_text === "[]"){

				ageBox.text("");

			}

		});

	};

	infoDeal.DeleteSqBK();


	function Toggle(obj){

		obj.click(function(){

			var This = $(this);

			var aBlock = This.next();
			
			if(This.children().text() == "+"){

				This.children().text("-");

				aBlock.show();

				obj.flag = true;

			}else{

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

	function AddedInfoHandler(obj){

		var nextBro = obj.next();

		if(nextBro.css("display") === "none"){

			obj.children("span").text("-");

			nextBro.show();

		}else{

			obj.children("span").text("+");

			nextBro.hide();

		}
	}

	//tracking-link click event

	$(".tracking-link").on('click', function(){

		AddedInfoHandler($(this));

	});

	//comment-link click event

	$(".comment-link").on('click', function(){

		AddedInfoHandler($(this));

	});

	//show more experience

	$('.show-more').on('click', function(){

		var text = $(this).text();

		if( text.indexOf('展开') !== -1 ){

			$(this).parent().find('.experience-hide').css({

				'display' : 'block'

			});

			$(this).text('折叠');

		}else{

			$(this).parent().find('.experience-hide').css({

				'display' : 'none'

			});

			$(this).text('展开');

		}

	});

});