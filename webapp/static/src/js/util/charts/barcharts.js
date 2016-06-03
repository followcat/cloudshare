define(['./lib/echarts'], function(echarts){

    //Define BarChart object
    function BarChart(elementId){
        this.elementId = elementId;
        this.charts = echarts.init(document.getElementById(elementId));
        this.charts.showLoading({
            text: '数据加载中...',
            effect: 'whirling',
            textStyle: {
                fontSize: 20
            }
        });
    }

    //Define function
    BarChart.prototype.makeBar = function(jsonData){
        //judge json data type, if string, translate to json object
        if (typeof jsonData === 'string') {
            jsonData = JSON.parse(jsonData);
        }else if(typeof jsonData === 'array') {
            jsonData = JSON.stringify(jsonData);
        }else if (typeof jsonData === 'undefined') {
            return 'Json data is undefined'
        }
        var option = getOption(jsonData);
        setCharts(this.charts, option);
    }

    function setCharts(charts, option){
        charts.hideLoading();
        charts.setOption(option);
    }

    function getCategory(jsonData){
        var list = [];

        for(var index in jsonData){
            list.push(index);
        }

        return list;
    }

    function getSeriesData(jsonData){
        var list = [];

        for(var index in jsonData){
            list.push(jsonData[index].length);
        }

        return list;
    }

    function getOption(jsonData){
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
                    dataView: {
                        show: true,
                        readOnly: true
                    },
                    magicType: {
                        show: true,
                        type: ['line', 'bar']
                    },
                    restore: {
                        show: true
                    },
                    saveAsImage: {
                        show: true
                    }
                }
            },
            xAxis: [{
                type: 'category',
                // axisLabel: {
                //     rotate: 20
                // },
                data: getCategory(jsonData)
            }],
            yAxis: [{
                type: 'value'
            }],
            series:[
                {
                    name: '数量',
                    type: 'bar',
                    data: getSeriesData(jsonData)
                }
            ]
        };

        return option;
    }

    return function(elementId){
        return new BarChart(elementId)
    }
});
