'use strict';

/**
 * 对职位描述中的每个item进行换行处理
 * @param  {number} beginIndex [字符串截取开始的位置]
 * @param  {number} cutNumber  [间隔的字符串个数]
 * @param  {string} string     [需要进行处理的目标字符串]
 * @return {string} [返回换行后的字符串]
 */
const processString = (beginIndex, cutNumber, string) => {
  if (beginIndex > string.length) {
    return '';
  } else {
    return string.substr(beginIndex, cutNumber) + '\n' + processString(beginIndex+cutNumber, cutNumber, string);
  }
};

/**
 * 获取符合echarts图例 legend API格式数据
 * @param  {array} data [由后台获取到的数据]
 * @return {array} [处理后的legend数组]
 */
const getLegend = (data) => {
  return data.map(item => {
    return item.name || item.id;
  });
};

/**
 * 获取符合echarts雷达图指示器和系列数据API格式的数据
 * @param  {array} data [由后台获取的数据]
 * @param  {number} max [指示器的最大值]
 * @return {object} [返回包含指示器数组和系列对象的对象]
 */
const getIndicatorAndSeries = (data, max) => {
  let object = {
    indicator: [],
    series: {},
  };

  for (let i = 0, dLen = data.length; i < dLen; i++) {
    let current = data[i],
        value = [];

    object.indicator.push({ name: current.description, max: max });

    for (let j = 0,  cLen = current.value.length; j < cLen; j++) {
      let name = current.value[j].name || current.value[j].id;
      let value = object.series[name] || [];
      value.push(current.value[j].match);
      object.series[name] = value;
    }
  }

  return object;
};

/**
 * 根据请求的数据结果生成雷达图的配置对象
 * @param  {number} max  [雷达图坐标的最大值]
 * @param  {array]} data [请求的数据结果集]
 * @return {object} option [返回雷达图配置对象]
 */
const getRadarOption = (max, data, cutNumber = 20) => {
  const legend = getLegend(data[0].value),
        indicatorAndSeries = getIndicatorAndSeries(data, max),
        indicator = indicatorAndSeries.indicator,
        series = indicatorAndSeries.series;

  const option = {
    title: {
      text: 'Charts',
    },
    tooltip: {
      trigger: 'item',
      position: 'inside',
      formatter: function (param, ticket, callback) {
        const value = param.value;
        let content = '';
        for ( let i = 0; i < indicator.length; i++) {
          let name = indicator[i].name;
          if (name.length > 50) {
            name = `${name.substr(0, 50)}...`;
          }
          content += `${name}: ${Math.round(value[i])} <br />`;
        }
        return content;
      },
      textStyle: {
        fontSize: 12,
      },
    },
    legend: {
      orient: 'horizontal',
      x: 'right',
      y: 'bottom',
      data: legend,
    },
    toolbox: {
      show: true,
      feature: {
        saveAsImage: {
          show: true,
          pixelRatio: 1.5,
        },
      },
    },
    radar: {
      radius: '70%',
      name: {
        formatter: function (value, indicator) {
          return processString(0, cutNumber, value);
        },
        textStyle: {
          color: '#5B5B5B',
        }
      },
      indicator: indicator,
    },
    calculable: true,
    series: [{
      type: 'radar',
      data: legend.map(item => { return { name: item, value: series[item] } }),
    }],
  };

  return option;
};

/**
 * 对外部输出函数变量
 */
export { getRadarOption };
