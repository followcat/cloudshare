define(['../js/lib/echarts'], function(echarts) {
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
    RadarChart.prototype.makeRadar = function(jsonData){
        //judge json data type, if string, translate to json object
        if (typeof jsonData == 'string') {
            jsonData = JSON.parse(jsonData);
        } else if (typeof jsonData == 'undefined') {
            return 'Json data is undefined'
        }

        var option = getOption(jsonData);  //get the radar charts option
        setCharts(this.charts, option);    //set radar charts
    }

    //Setup the charts
    function setCharts(charts, option) {
        charts.hideLoading();   //close loading animate
        charts.setOption(option);   //call echart api setoption
    }

    //Make legend list
    function getLegendList(jsonData) {
        var list = [];

        for (var index in jsonData) {
            list.push(index);
        }

        return list;
    }

    //Make indicator list
    function getIndicator(jsonData) {
        var keyArr = [],
            max = 0;

        for (var index in jsonData) {
            for (var i = 0, len = jsonData[index].length; i < len; i++) {
                if (keyArr.indexOf(jsonData[index][i]['key']) < 0) {
                    keyArr.push(jsonData[index][i]['key']);
                }

                if (jsonData[index][i]['value'] > max) {
                    max = parseInt(jsonData[index][i]['value']);
                }
            }
        }

        var array = [];

        for (var j = 0, len = keyArr.length; j < len; j++) {
            var obj = Object();

            obj.text = keyArr[j];
            obj.max = max;
            array.push(obj);
            obj = null;
        }

        return array;
    }

    function getSeriesData(jsonData) {
        var list = [];

        for (var index in jsonData) {
            var obj = Object();

            obj.name = index;
            obj.value = [];

            for (var i = 0, len = jsonData[index].length; i < len; i++) {
                obj.value.push(parseInt(jsonData[index][i]['value']));
            }

            list.push(obj);
            obj = null;
        }

        return list;
    }

    function getOption(jsonData) {
        var option = {
            title: {
                text: 'Radar'
            },
            tooltip: {
                trigger: 'item',
                position: 'bottom',
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
                        show: true
                    }
                }
            },
            radar: [{
                indicator: getIndicator(jsonData)
            }],
            calculable: true,
            series: [{
                type: 'radar',
                data: getSeriesData(jsonData)
            }]
        };

        return option;
    }

    return function(elementId){
        return new RadarChart(elementId);
    }
});