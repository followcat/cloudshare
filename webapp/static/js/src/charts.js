define(['../lib/source/echarts','echarts/theme/macarons', 'echarts/chart/radar'], function(ec){

    /*
    JSON data format:
    {
        "arg": [
            {
                "key": key,
                "value": value
            }
        ]
    }
    */
    function chart(elementId, chartType, jsonData){
        var result;

        if(typeof jsonData == 'string'){
            jsonData = JSON.parse(jsonData);
        }else if(typeof jsonData == 'undefined'){
            return 'Json data is undefined'
        }

        switch (chartType){
            case 'radar':
                result = makeRadar(elementId, jsonData);
        }

        return result;
    }

    function setCharts(elementId, option){
        var chart = ec.init(document.getElementById(elementId), 'macarons');

        chart.showLoading({
            text: '加载中...',
            effect: 'whirling',
            textStyle: {
                fontSize: 20
            }
        });

        chart.hideLoading();
        chart.setOption(option);
    }

    function getLegendList(jsonData){
        var list = [];
        for(var index in jsonData){
            list.push(index);
        }
        return list;
    }

    function getIndicator(jsonData){
        var keyArr = [], max = 0;

        for(var index in jsonData){
            for(var i = 0, len = jsonData[index].length; i < len; i++){
                if(keyArr.indexOf(jsonData[index][i]['key']) < 0){
                    keyArr.push(jsonData[index][i]['key']);
                }

                if(jsonData[index][i]['value'] > max){
                    max = jsonData[index][i]['value'];
                }
            }
        }

        var array = [];
        for(var j = 0, len = keyArr.length; j < len; j++){
            var obj = {};
            obj.text = keyArr[j];
            obj.max = max;
            array.push(obj);
            obj = null;
        }

        return array;
    }

    function getSeriesData(jsonData){
        var list = [];

        for(var index in jsonData){
            var obj = {};
            obj.name = index;
            obj.value = [];
            for(var i = 0, len = jsonData[index].length; i < len; i++){
                obj.value.push(parseInt(jsonData[index][i]['value']));
            }
            list.push(obj);
            obj = null;
        }

        return list;
    }

    function makeRadar(elementId, jsonData){
        var option = {
            title: {
                text: 'vs'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                orient: 'vertical',
                x: 'right',
                y: 'center',
                data: getLegendList(jsonData)
            },
            toolbox: {
                show: true,
                feature: {
                    mark: {show: true},
                    dataView : {show: true, readOnly: false},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            polar: [
                {
                    indicator: getIndicator(jsonData)
                }
            ],
            calculable: true,
            series: [
                {
                    type: 'radar',
                    data: getSeriesData(jsonData)
                }
            ]
        };

        setCharts(option);

    }

    return chart;
});