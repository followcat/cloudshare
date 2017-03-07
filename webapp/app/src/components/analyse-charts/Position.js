'use strict';
import React, { Component, PropTypes } from 'react';

import Charts from './Charts';

import { Button, Modal } from 'antd';

import { getPositionData } from 'request/analyse';

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

class Position extends Component {
  constructor() {
    super();
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
        text: '职位分析'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer : {
          type : 'shadow'
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
    const { keyword } = this.props;

    this.setState({
      visible: true,
      data: [],
    });

    getPositionData({
      search_text: keyword
    }, json => {
      if (json.code === 200) {
        const data = json.data.sort(compare),
              option = this.getOption(data);
        
        this.setState({
          data: data,
          option: option,
        });
      }
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  render() {
    const { style } = this.props,
          { visible, data, option } = this.state;

    return (
      <div style={style}>
        <Button onClick={this.handleClick}>职位分析</Button>
        <Modal
          title="图表"
          visible={visible}
          onCancel={this.handleCancel}
          footer={[
            <Button type="ghost" size="large" onClick={this.handleCancel}>取消</Button>
          ]}
          style={{ top: 20 }}
          width={980}
        >
          {data.length > 0 ?
            <Charts option={option} style={{ width: 900, height: 460, margin: '0 auto' }} /> :
            ''}
        </Modal>
      </div>
    );
  }
}

Position.propTypes = {
  style: PropTypes.object,
  keyword: PropTypes.string
};

export default Position;
