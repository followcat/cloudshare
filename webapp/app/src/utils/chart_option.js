'use strict';

/**
 * 根据请求的数据结果生成雷达图的配置对象
 * @param  {[number]} max  [雷达图坐标的最大值]
 * @param  {[array]} data [请求的数据结果集]
 * @return {[object]} option [返回雷达图配置对象]
 */
const getRadarOption = (max, data) => {
  console.log(max);
  console.log(data);
  const legend = data[0].value.map(item => {
    return item.name ? item.name : item.id;
  });

  const indicator = [],
        seriesData = {};

  for (let i = 0, rLen = data.length; i < rLen; i++) {
    let current = data[i],
        value = [];

    indicator.push({ name: current.description, max: max });

    for (let j = 0,  cLen = current.value.length; j < cLen; j++) {
      let name = current.value[j].name ? current.value[j].name : current.value[j].id;
      let value = seriesData[name] ? seriesData[name] : [];
      value.push(current.value[j].match);
      seriesData[name] = value;
    }
  }

  const option = {
    title: {
      text: 'Charts',
    },
    tooltip: {
      trigger: 'item',
      position: 'bottom',
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
      indicator: indicator,
    },
    textStyle: {
      fontStyle: 'bolder',
      fontSize: 14
    },
    calculable: true,
    series: [{
      type: 'radar',
      data: legend.map(item => { return { name: item, value: seriesData[item] } }),
    }],
  };

  return option;
};

/**
 * 对外部输出函数变量
 */
export { getRadarOption };
