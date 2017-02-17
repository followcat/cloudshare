'use strict';
import React, { Component, PropTypes } from 'react';

import Charts from './Charts';

import { Button, Modal } from 'antd';

import { getExperienceData } from 'request/analyse';

class Experience extends Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: false,
      data: [],
      option: {},
    };
    this.getOption = this.getOption.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  getOption(data) {
    const option = {
      title: { text: '能力分布' },
      tooltip: {
        trigger: 'item',
      },
      toolbox: {
        feature: {
          dataZoom: { show: true },
          saveAsImage: { show: true },
        },
      },
      xAxis: [{
        type: 'value',
        name: '工作年限',
        scale: true,
      }],
      yAxis: [{
        type: 'value',
        name: '经历值',
        scale: true,
      }],
      series: [{
        type: 'scatter',
        data: data,
      }],
    };

    return option;
  }

  handleClick() {
    const { dataSource } = this.props;

    this.setState({
      visible: true,
      data: [],
    });

    getExperienceData({
      md_ids: dataSource.map(item => item.cv_id)
    }, json => {
      if (json.code === 200) {
        const data = json.data.map((item) => [item.experience.work_year, item.experience.experience_value]),
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
    const { style } = this.props;

    return (
      <div style={style}>
        <Button onClick={this.handleClick}>工作经验分析</Button>
        <Modal
          title="图表"
          visible={this.state.visible}
          onCancel={this.handleCancel}
          footer={[
            <Button type="ghost" size="large" onClick={this.handleCancel}>取消</Button>
          ]}
          style={{ top: 20 }}
          width={980}
        >
          {this.state.data.length > 0 ?
            <Charts option={this.state.option} style={{ width: 900, height: 460, margin: '0 auto' }} /> :
            ''}
        </Modal>
      </div>
    );
  }
}

Experience.propTypes = {
  style: PropTypes.object,
  dataSource: PropTypes.array
};

export default Experience;
