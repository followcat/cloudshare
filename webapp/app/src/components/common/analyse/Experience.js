'use strict';
import React, { Component, PropTypes } from 'react';

import { Button, Modal } from 'antd';

import Charts from '../Charts';

import 'whatwg-fetch';

export default class Experience extends Component {
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
      title: { text: 'Ability' },
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
        name: 'Work Years',
        scale: true,
      }],
      yAxis: [{
        type: 'value',
        name: 'Experience Values',
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
    this.setState({
      visible: true,
      data: [],
    });

    const _this = this;
    
    fetch(`/api/mining/experience`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        md_ids: this.props.dataSource.map(item => item.cv_id)
      }),
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        const data = json.data.map((item) => [item.experience.work_year, item.experience.experience_value]),
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
      <div>
        <Button type="primary" onClick={this.handleClick}>Show Work Experience</Button>
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