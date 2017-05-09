'use strict';
import React, { Component, PropTypes } from 'react';
import echarts from 'echarts';
import { Button, Layout } from 'antd';

import { API } from 'API';
import { getDocWrodMining } from 'request/docmining';


class ParallelNutrients extends Component {

  componentDidMount() {
    this.init();
  }

  componentDidUpdate() {
    if (this.state.data.length !== 0) {
      this.parallelnutrients.setOption(this.state.option);
    };
  }

  componentUnMount() {
    this.dispose();
  }

  init() {
    this.parallelnutrients = echarts.init(this.refs.parallelnutrients);
  }

  constructor() {
    super();
    this.state = {
      data: [],
      option: {},
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    const { postData } = this.props;
    getDocWrodMining(API.ANALYSIS_BY_DOC_WORD_API, postData, json => {
        if (json.code === 200) {
          var data = json.data;
          this.normalizeData(data);
          this.setState({
            data: json.data,
            option: this.getOption(data),
          });
        }
      });
  }

  groupCategories = [];
  groupColors = [];

  normalizeData(originData) {
      this.groupCategories = [];
      this.groupColors = [];
      var indices = {
        name: 1,
        group: 0,
        id: 17
      };
      var groupMap = {};
      originData.forEach(function (row) {
          var groupName = row[indices.group];
          if (!groupMap.hasOwnProperty(groupName)) {
              groupMap[groupName] = 1;
          }
      });

      originData.forEach(function (row) {
          row.forEach(function (item, index) {
              if (index !== indices.name
                  && index !== indices.group
                  && index !== indices.id
              ) {
                  // Convert null to zero, as all of them under unit "g".
                  row[index] = parseFloat(item) || 0;
              }
          });
      });

      for (var groupName in groupMap) {
          if (groupMap.hasOwnProperty(groupName)) {
              this.groupCategories.push(groupName);
          }
      }
      var hStep = Math.round(300 / (this.groupCategories.length - 1));
      for (var i = 0; i < this.groupCategories.length; i++) {
          this.groupColors.push(echarts.color.modifyHSL('#5A94DF', hStep * i));
      }
  }

  getOption(data) {
      var indices = {
        name: 1,
        group: 0,
        id: 17
      };
      var schema = new Array(data.lenght);
      for(var i=0;i<data[0].length;i++){
          schema[i] = {name: 'T'+i, index: i}
      }
      var schema = [
          {name: 'name', index: 0},
          {name: 'group', index: 1},
          {name: 'protein', index: 2},
          {name: 'calcium', index: 3},
          {name: 'sodium', index: 4},
          {name: 'fiber', index: 5},
          {name: 'vitaminc', index: 6},
          {name: 'potassium', index: 7},
          {name: 'carbohydrate', index: 8},
          {name: 'sugars', index: 9},
          {name: 'fat', index: 10},
          {name: 'water', index: 11},
          {name: 'calories', index: 12},
          {name: 'saturated', index: 13},
          {name: 'monounsat', index: 14},
          {name: 'polyunsat', index: 15},
          {name: 'id', index: 16}
      ];

      var lineStyle = {
          normal: {
              width: 1.5,
              opacity: 0.35
          }
      };

      return {
          backgroundColor: '#333',
          tooltip: {
              padding: 10,
              backgroundColor: '#222',
              borderColor: '#777',
              borderWidth: 1,
              formatter: function (obj) {
                  var value = obj[0].value;
                  return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                      + schema[1].name + '：' + value[1] + '<br>'
                      + schema[2].name + '：' + value[2] + '<br>'
                      + schema[3].name + '：' + value[3] + '<br>'
                      + schema[4].name + '：' + value[4] + '<br>'
                      + schema[5].name + '：' + value[5] + '<br>'
                      + schema[6].name + '：' + value[6] + '<br>';
              }
          },
          title: [
              {
                  text: 'Analysis & Optimization',
                  top: 0,
                  left: 0,
                  textStyle: {
                      color: '#fff'
                  }
              }
          ],
          visualMap: {
              show: true,
              type: 'piecewise',
              categories: this.groupCategories,
              dimension: indices.group,
              inRange: {
                  color: this.groupColors //['#d94e5d','#eac736','#50a3ba']
              },
              outOfRange: {
                  color: ['#ccc'] //['#d94e5d','#eac736','#50a3ba']
              },
              top: 20,
              textStyle: {
                  color: '#fff'
              },
              realtime: true
          },
          parallelAxis: [
              {dim: 16, name: schema[16].name, scale: true, nameLocation: 'end'},
              {dim: 2, name: schema[2].name, nameLocation: 'end'},
              {dim: 4, name: schema[4].name, nameLocation: 'end'},
              {dim: 3, name: schema[3].name, nameLocation: 'end'},
              {dim: 5, name: schema[5].name, nameLocation: 'end'},
              {dim: 6, name: schema[6].name, nameLocation: 'end'},
              {dim: 7, name: schema[7].name, nameLocation: 'end'},
              {dim: 8, name: schema[8].name, nameLocation: 'end'},
              {dim: 9, name: schema[9].name, nameLocation: 'end'},
              {dim: 10, name: schema[10].name, nameLocation: 'end'},
              {dim: 11, name: schema[11].name, nameLocation: 'end'},
              {dim: 12, name: schema[12].name, nameLocation: 'end'},
              {dim: 13, name: schema[13].name, nameLocation: 'end'},
              {dim: 14, name: schema[14].name, nameLocation: 'end'},
              {dim: 15, name: schema[15].name, nameLocation: 'end'}
          ],
          parallel: {
              left: 280,
              top: 20,
              // top: 150,
              // height: 300,
              width: 600,
              layout: 'vertical',
              parallelAxisDefault: {
                  type: 'value',
                  name: 'nutrients',
                  nameLocation: 'end',
                  nameGap: 30,
                  nameTextStyle: {
                      color: '#fff',
                      fontSize: 10
                  },
                  axisLine: {
                      lineStyle: {
                          color: '#aaa'
                      }
                  },
                  axisTick: {
                      lineStyle: {
                          color: '#777'
                      }
                  },
                  splitLine: {
                      show: false
                  },
                  axisLabel: {
                      textStyle: {
                          color: '#fff'
                      }
                  },
                  realtime: false
              }
          },
          animation: true,
          series: [
              {
                  name: 'nutrients',
                  type: 'parallel',
                  lineStyle: lineStyle,
                  inactiveOpacity: 0,
                  activeOpacity: 0.01,
                  progressive: 500,
                  smooth: true,
                  data: data
              }
          ]
      };
    }

  render() {
    const { data, option } = this.state;

    return (
      <Layout>
       <Button type="primary" onClick={this.handleClick}>分析作用</Button>
        <div ref="parallelnutrients"
             style={{ width: 1078, height: 460, margin: '0 auto' }}>
        </div>
      </Layout>
    );
  }
}

ParallelNutrients.propTypes = {
  postData: PropTypes.object
};

export default ParallelNutrients;
