define(['./lib/js/echarts'], function(echarts) {
/*JSON data format:
    {
        "arg": [
            {
                "key": key,
                "value": value
            }
        ]
    }
*/
    //Define a radar object
    function RadarChart(elementId){
        //init
        this.elementId = elementId;
        this.charts = echarts.init(document.getElementById(elementId));

        //loading animate
        this.charts.showLoading({
            text: '加载中...',
            effect: 'whirling',
            textStyle: {
                fontSize: 20
            }
        });
    }

    //Define RadarChart
    RadarChart.prototype.makeRadar = function(datas, max){
        //judge json data type, if string, translate to json object
        if (typeof datas === 'string') {
            datas = JSON.parse(datas);
        } else if (typeof datas === 'undefined') {
            return 'Json data is undefined'
        }

        var option = getOption(datas, max);  //get the radar charts option
        setCharts(this.charts, option);    //set radar charts
    }

    //Setup the charts
    function setCharts(charts, option) {
        charts.hideLoading();   //close loading animate
        charts.setOption(option);   //call echart api setoption
    }

    //Make legend list
    function getLegendList(datas) {
        var list = [],
            values = datas[0]['value'];

        for (var i = 0, valuesLen = values.length; i < valuesLen; i++) {
            if (values[i]['name'] !== ''){
                list.push(values[i]['name']);
            }else{
                list.push(values[i]['filename']);
            }
        }

        return list;
    }

    //Make indicator list
    function getIndicator(datas, max) {
        var indicatorArr = [];

        for (var i = 0, datasLen = datas.length; i < datasLen; i++){
            var obj = new Object(),
                short_jd = '',
                jdStr = datas[i]['description'];
            if ( jdStr.length > 16 ) {
                short_jd = jdStr.slice(0, 17) + '...'
            } else {
                short_jd = jdStr;
            }
            obj.name = short_jd;

            obj.max = max;
            indicatorArr.push(obj);
            obj = null;
        }

        return indicatorArr;
    }

    function getSeriesData(datas) {
        var list = [],
            flag = false;

        var valuesLen = datas[0]['value'].length;
        for (var i = 0; i < valuesLen; i++){
            var obj = new Object();
            obj.value = [];

            for ( var j = 0, datasLen = datas.length; j < datasLen; j++){
                var match = datas[j]['value'][i]['match'];
                obj.value.push(parseInt(match));
                if(!obj['name']){
                    obj['name'] = datas[j]['value'][i]['name'];
                }else{
                    continue;
                }
            }

            list.push(obj);
            obj = null;
        }

        return list;
    }

    function getOption(datas, max) {
        var option = {
            title: {
                text: 'Radar'
            },
            tooltip: {
                trigger: 'item',
                position: 'bottom',
            },
            legend: {
                orient: 'horizontal',
                x: 'right',
                y: 'bottom',
                data: getLegendList(datas)
            },
            toolbox: {
                show: true,
                feature: {
                    mark: {
                        show: true
                    },
                    dataView: {
                        show: true,
                        readOnly: false
                    },
                    restore: {
                        show: true
                    },
                    saveAsImage: {
                        show: true,
                        pixelRatio: 1.5
                    }
                }
            },
            radar: {
                indicator: getIndicator(datas, max)
            },
            textStyle: {
                fontStyle: 'bolder',
                fontSize: 14
            },
            calculable: true,
            series: [{
                type: 'radar',
                data: getSeriesData(datas)
            }]
        };

        return option;
    }

    return function(elementId){
        return new RadarChart(elementId);
    }
});
