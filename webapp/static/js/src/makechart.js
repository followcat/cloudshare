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
		'echarts/chart/radar', 
		'bootstrap', 
		'header', 
		'formvalidate', 
		'Upload',
	], function($, ec){

//set params input disabled

$('.open-btn').on('click', function(){

	 if($(this).text() === '开启' && $(this).prev().attr('disabled')){

    $(this).prev().removeAttr('disabled');

    $(this).text('关闭');

  }else{

  	 $(this).prev().attr('disabled','disabled');

    $(this).text('开启');

  }
});


//submit params input

$('#submit-params').on('click', function(){
  
  $('table tr').remove();

  var paramsArr = ['姓名'];

  var paramsEle = $('.param');

  var standard = ['<input type=\'text\' class=\'form-control input-sm\' value=\'标准\' >'];

  for (var i = 0, len = paramsEle.length - 1; i < len; i++) {

    if( !$(paramsEle[i]).attr('disabled') ){

      paramsArr.push($(paramsEle[i]).val());
      
      standard.push('<input type=\'text\' class=\'form-control input-sm\' value=\'\' >');

    }

  }
  
  paramsArr.push('#');

  standard.push('<button type=\'button\' class=\'btn btn-default btn-sm delete\'>delete</button>');

  var thStr = '';
  
  var tdStr = '';
  // $('table thead').append('<tr></tr>');

  for(i = 0, len = paramsArr.length; i < len; i++){

    var str = '<th>'+ paramsArr[i] +'</th>';
    
    var standardStr = '<td>' + standard[i] + '</td>';

    thStr += str;

    tdStr += standardStr;

  }
  
  $('table thead').append('<tr>'+ thStr +'</tr>');

  $('table tbody').append('<tr>'+ tdStr +'</tr>');

});


//add table row

$('#add-row').on('click', function(){
  
  var column = $('table thead tr').children().length;
  
  var tdStr = '';

  for(var i = 0; i < column - 1; i++){
    tdStr += '<td><input type=\'text\' class=\'form-control input-sm\' value=\'\' ></td>';
  }
  
  tdStr += '<td><button type=\'button\' class=\'btn btn-default btn-sm delete\'>delete</button></td>';

  $('table tbody').append('<tr>'+ tdStr +'</tr>');

});


$('table tbody').delegate('.delete', 'click', function(){
  
  $(this).parent().parent().remove();

});


var getKeyArr = function(){
  
  var arr = [];

  var thEle = $('table thead tr th');

  for(var i = 0, len = thEle.length; i < len-1; i++){

    arr.push($(thEle[i]).text());

  }

  return arr;

};


function getPersonObjArr(){

  var arr = [];

  var trEle = $('table tbody tr');

  for(var i = 0; i < trEle.length; i++){
    
    var tdELe = $(trEle[i]).children('td'); 
    
    var person = new Object();

    var valArr = [];

    for(var j = 0, len = tdELe.length; j < len - 1; j++){
      
      if(j === 0){

        person.name = $(tdELe[j]).find('input').val();

      }else{
        
        valArr.push(parseInt($(tdELe[j]).find('input').val()));

      }

    }

    person.value = valArr;

    arr.push(person);

  }

  return arr;

}


function getIndicator(keyArr, personArr){

  var arr = [];

  for(var i = 1, len = keyArr.length; i < len; i++){

    var max = 0;

    for(var j = 0, personLen = personArr.length; j < personLen; j++){

      if( personArr[j].value[i-1] > max){

        max = personArr[j].value[i-1];

      }

    }

    var obj = {};

    obj.text = keyArr[i];

    obj.max = parseInt(max);

    arr.push(obj);

    obj = null;

  }

  return arr;

}


$('#make-chart-btn').on('click', function(){
  
  var charts = ec.init(document.getElementById('chart-wrap'), 'macarons');
  
  charts.showLoading({

				text: '加载中...',

				effect: 'whirling',

				textStyle: {

					fontSize: 20

				}
	});

  var keyArr = getKeyArr();

  var personArr = getPersonObjArr();

  var indicator = getIndicator(keyArr, personArr);

  var option = {
    title : {
        subtext: '预算 vs 开销（Budget vs spending)\nasdasd',
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        orient : 'vertical',
        x : 'left',
        y : 'bottom',
        data:function(){
          
          var list = [];

          for(var i = 0, len = personArr.length; i < len; i++){

            list.push(personArr[i].name);

          }

          return list;

        }()
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    polar : [
       {
           indicator : indicator
        }
    ],
    calculable : true,
    series : [
        {
            type: 'radar',
            data : function(){

              var list = [];
              
              for(var i = 0, len = personArr.length; i < len; i++){

                if(personArr[i].name === '标准' || i === 0){

                  var obj = {}, itemStyle = {}, normal = {}, lineStyle = {};

                  obj.name = personArr[i].name;
                  obj.value = personArr[i].value;
                  lineStyle.type = 'dashed';
                  normal.lineStyle = lineStyle;
                  itemStyle.normal = normal;
                  obj.itemStyle = itemStyle;

                  list.push(obj);

                }else{

                  list.push(personArr[i]);

                }
              }
              
              console.log(list);
              return list;

            }()
        }
    ]
  };

  charts.hideLoading();
                    
  charts.setOption(option);

});


});

/*

*/