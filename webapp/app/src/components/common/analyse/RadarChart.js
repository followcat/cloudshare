'use strict';
import React, { Component } from 'react';

import { Button, Modal } from 'antd';

import Charts from '../Charts';

import Immutable from 'immutable';

import Storage from '../../../utils/storage';
import Generator from '../../../utils/generator';
import 'whatwg-fetch';

export default class RadarChart extends Component {
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
    const result = data.result;
    const legend = result[0].value.map(item => {
      return item.name ? item.name : item.id;
    });

    const indicator = [],
          seriesData = {};

    for (let i = 0, rLen = result.length; i < rLen; i++) {
      let current = result[i],
          value = [];

      indicator.push({ name: current.description, max: data.max });

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
  }

  handleClick() {
    this.setState({
      visible: true,
      data: [],
    });

    const _this = this;

    fetch(`/api/mining/valuable`, {
      method: 'POST',
      credential: 'include',
      headers: {
        'Authorization': `Basic ${Storage.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        id: this.props.postData.id,
        name_list: this.props.selection.toJS().map(item => { return item.id + '.md' }),
        uses: this.props.postData.uses,
      }),
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        _this.setState({
          data: json.data.result,
          option: _this.getOption(json.data),
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
        <Button type="primary" onClick={this.handleClick}>Show Radar Chart</Button>
        <Modal
          title="Charts View"
          visible={this.state.visible}
          onCancel={this.handleCancel}
          footer={
            [<Button type="ghost" onClick={this.handleCancel}>Close</Button>]
          }
          style={{ top: 20 }}
          width={980}
        >
          {this.state.data.length > 0 ? <Charts option={this.state.option} style={{ width: 900, height: 460, margin: '0 auto' }} /> : ''}
        </Modal>
      </div>
    );
  }
}