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

	//Show position region button handle

	$('#vd-position-region').on('click', function(){

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

			var mdList = [];

			var titleList = $('.item-title');

			$.each(titleList, function(index, data){

				var mdId = $(data).attr('href').split('/')[2];

				mdList.push(mdId);

			});

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

				        data : regionObj.regionDataArr

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

			$.ajax({

				url: '/mining/position',

				type: 'get',

				data:{
					'search_text' : $('input[name="search_text"]').val()
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