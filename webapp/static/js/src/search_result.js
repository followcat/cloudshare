require.config({

    baseUrl: "../static/js",

    paths: {
        'jquery': 'lib/jquery',
        'bootstrap': 'lib/bootstrap',
        'header': 'src/header',
        'formvalidate': 'src/formvalidate',
        'Upload': 'src/upload',
        'radarcharts': 'src/charts/radarcharts',
        'barcharts': 'src/charts/barcharts',
        'scatters': "src/charts/scattercharts",
        'colorgrad': 'src/color/colorgrad'
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
        'bootstrap',
        'header',
        'formvalidate',
        'Upload'
    ],
    function($, radarcharts, barcharts, scattercharts, ColorGrad) {
        //Echarts - visualized data
        function isExist(array, value) {
            for (var i = 0, len = array.length; i < len; i++) {
                if (array[i].name === value) {
                    return i;
                }
            }

            return false;
        }

        //Show position region on the map

        //Deal with Md lists and its region source
        function GetRegionList(resultArr) {
            var regionDataArr = new Array();
            var geoObj = new Object();

            for (var i = 0, iLen = resultArr.length; i < iLen; i++) {
                var subArr = resultArr[i];
                for (var j = 0, jLen = subArr.length; j < jLen; j++) {
                    var obj = subArr[j];
                    //init regionDataArr 
                    if (obj.name) {
                        if (regionDataArr.length === 0) {
                            var regionObj = new Object();

                            regionObj.name = obj.name;
                            regionObj.value = 1;

                            geoObj[obj.name] = [obj.coord[0], obj.coord[1]];
                            regionDataArr.push(regionObj);
                            regionObj = null;
                        } else {
                            var index = isExist(regionDataArr, obj.name);
                            if (index || index === 0) {
                                regionDataArr[index].value += 1;
                            } else {
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
        function GetMdLists() {
            var mdList = [];
            var titleList = $('.item-title');
            $.each(titleList, function(index, data) {
                var mdId = $(data).attr('href').split('/')[2];
                mdList.push(mdId);
            });

            return mdList;
        }


        //Show position region button handle
        $('#vd-position-region').on('click', function() {
            $('#action-msg').text('');
            if ($('#data-main').css('display') === 'none') {
                $('#data-main').css('display', 'block');
                var positionCharts = echarts.init(document.getElementById('echarts-wrap'));
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
                    success: function(response) {
                        var regionObj = GetRegionList(response.result);
                        positionCharts.hideLoading();

                        var option = {
                            title: {
                                text: '职业分布情况',
                                x: 'center'
                            },
                            tooltip: {
                                trigger: 'item'
                            },
                            dataRange: {
                                min: 0,
                                max: 500,
                                calculable: true,
                                color: ['#191970', '#4D4D4D', '#551A8B', '#CD0000']
                            },
                            toolbox: {
                                show: true,
                                orient: 'vertical',
                                x: 'right',
                                y: 'center',
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
                            series: [{
                                name: 'region',
                                type: 'map',
                                mapType: 'china',
                                hoverable: false,
                                roam: true,
                                data: [],
                                markPoint: {
                                    symbolSize: 10, // 标注大小，半宽（半径）参数，当图形为方向或菱形则总宽度为symbolSize * 2
                                    itemStyle: {
                                        normal: {
                                            borderColor: '#87cefa',
                                            borderWidth: 1, // 标注边线线宽，单位px，默认为1
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
                                    data: function() {
                                        var list = [];
                                        for (var i = regionObj.regionDataArr.length - 1; i >= 0; i--) {
                                            if (regionObj.regionDataArr[i].value > 2) {
                                                list.push(regionObj.regionDataArr[i]);
                                            } else {
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
            } else {
                $('#data-main').css('display', 'none');
            }
        });

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
            var dataObj = new Object();
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
                    formdata['search_text'] = '公司';
                    formdata['md_ids'] = JSON.stringify(GetMdLists());
                } else {
                    formdata['search_text'] = $('#search_text').val();
                }
                $.ajax({
                    url: '/mining/position',
                    type: 'post',
                    data: formdata,
                    success: function(response) {
                        if (response.result !== '') {
                            var dataArr = dealPosition(response.result);
                            barchart.makeBar(dataArr);
                            barchart.charts.on('click', function(params) {
                                $('#action-msg').html('');
                                var name = params.name;
                                var str = '';
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

            };

            return dataArr;

        }

        //get Proportion point data

        function getProPointData(result) {
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
            var workingYear = parseInt(time / 12);
            var workingMonth = time % 12;
            var workingTime = changeTwoDecimal(workingYear + (workingMonth / 100));

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
            };

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
            if (text.indexOf('展开') !== -1) {
                $(this).parent().find('.experience-hide').css({'display': 'block'});
                $(this).text('折叠');
            } else {
                $(this).parent().find('.experience-hide').css({'display': 'none'});
                $(this).text('展开');
            }
        });


        function getNameLists(checkboxLists){
            var nameLists = [];
            for(var i = 0, len = checkboxLists.length; i < len; i++){
                if ( $(checkboxLists[i]).is(':checked') ){
                    nameLists.push($(checkboxLists[i]).next().attr('href').split('/')[2])
                }else{
                    continue;
                }
            }
            return nameLists;
        }

        $('#vd-valuable').on('click', function() {
            if ($('#data-main').css('display') === 'none') {
                $('#data-main').css('display', 'block');

                var checkboxLists = $('.checkbox-name');           
                var nameLists = getNameLists(checkboxLists);
                var radar = radarcharts('echarts-wrap');
                if( nameLists.length > 0){
                    $.ajax({
                        url: '/analysis/valuable',
                        type: 'post',
                        data: {
                            'search_textarea': $('#search_textarea').text(),
                            'name_list': JSON.stringify(nameLists)
                        },
                        success: function(response) {
                            radar.makeRadar(response.data);
                        }
                    });
                }else{
                    $.ajax({
                        url: '/analysis/valuable',
                        type: 'get',
                        data: {
                            'search_textarea': $('#search_textarea').text()
                        },
                        success: function(response) {
                            radar.makeRadar(response.data);
                        }
                    });
                }                
            }else{
                $('#data-main').css('display', 'none');
            }
        });

        //Color Gradient according the score
        var itemLink = $('.item-link');
        var colorgrad = ColorGrad();
        for(var i = 0, len = itemLink.length; i < len; i++){
            var match = $(itemLink[i]).children('p').text();
            if (match === ''){
                break;
            }

            var matchToNum = parseFloat(match);
            var grad = colorgrad.gradient(parseInt(matchToNum*100));
            $(itemLink[i]).children('a').css({'color': grad});
        }
    });