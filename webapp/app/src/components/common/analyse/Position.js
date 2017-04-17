'use strict';
import React, { Component, PropTypes } from 'react';

import { Button, Modal } from 'antd';

import Charts from '../Charts';

import Storage from '../../../utils/storage';
import Generator from '../../../utils/generator';

import 'whatwg-fetch';

const compare = (value1, value2) => {
  let valueLen1 = value1.id_list.length,
      valueLen2 = value2.id_list.length;

  if (valueLen1 < valueLen2) {
    return 1;
  } else if (valueLen1 > valueLen2) {
    return -1;
  } else {
    return 0;
  }
};

const topNine = (data) => {
  if (data.length > 9) {
    return data.splice(0, 9);
  } else {
    return data;
  }
};

export default class Position extends Component {
  
  constructor(props) {
    super(props);

    this.state = {
      data: [],
      visible: false,
      option: {},
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  getOption(data) {
    const option = {
      title: {
        text: 'Position'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
          type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
      },
      toolbox: {
        show: true,
        feature: {
          magicType: {
            show: true,
            type: ['line', 'bar']
          },
          saveAsImage: {
            show: true
          }
        }
      },
      xAxis: [{
        type: 'category',
        data: topNine(data.map(item => item.position_name)),
        axisTick: {
          alignWithLabel: true
        }
      }],
      yAxis: [{
        type: 'value'
      }],
      series:[
        {
          name: 'Count',
          type: 'bar',
          data: topNine(data.map(item => item.id_list.length))
        }
      ]
    };

    return option;
  }

  handleClick() {
    this.setState({
      visible: true,
      data: [],
    });

    const _this = this;
    
    fetch(`/api/mining/position`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${Storage.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        'search_text': this.props.keyword,
      })
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        const data = json.data.sort(compare),
              option = _this.getOption(data);
        _this.setState({
          data: data,
          option: option,
        });
      }
    })
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  render() {
    return (
      <div style={this.props.style}>
        <Button type="primary" onClick={this.handleClick}>Show No. of Positions</Button>
        <Modal
          title="Charts View"
          visible={this.state.visible}
          onCancel={this.handleCancel}
          footer={[
            <Button type="ghost" size="large" onClick={this.handleCancel}>Cancel</Button>
          ]}
          style={{ top: 20 }}
          width={980}
        >
          {this.state.data.length > 0 ? <Charts option={this.state.option} style={{ width: 900, height: 460, margin: '0 auto' }} /> : ''}
        </Modal>
      </div>
    );
  }
}