define(function(){

    //Define ScatterChart object
    function ScatterChart(elementId){
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

    ScatterChart.prototype.makeScatter = function(jsonData){
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

        //Handle events
        charts.on('click', function(params) {
            var filename = params.name;
            var a = $("<a href=\'\/show\/" + filename + "\' target=\'_blank\'><\/a>").get(0);
            var e = document.createEvent('MouseEvents');
            e.initEvent('click', true, true);
            a.dispatchEvent(e);
        });
    }

    function getSeriesData(jsonData){
        var list = [];
        for(var i = 0, len = jsonData.length; i < len; i++){
            var dataObj = new Object();
            dataObj.name = jsonData[i].fileName;
            dataObj.value = jsonData[i].data;
            list.push(dataObj);
            dataObj = null;
        }
        return list;
    }

    function getOption(jsonData){
        var option = {
            title: {
                text: '能力分布'
            },
            tooltip: {
                trigger: 'axis',
                showDelay: 0,
                axisPointer: {
                    show: true,
                    type: 'cross',
                    lineStyle: {
                        type: 'dashed',
                        width: 1
                    }
                }
            },
            toolbox: {
                show: true,
                feature: {
                    mark: {
                        show: true
                    },
                    dataZoom: {
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
            xAxis: [{
                type: 'value',
                scale: true
            }],
            yAxis: [{
                type: 'value',
                scale: true
            }],
            series: [{
                name: 'test',
                type: 'scatter',
                data: getSeriesData(jsonData)
            }]


        };
        return option;
    }

    return function(elementId){
        return new ScatterChart(elementId);
    }
});
