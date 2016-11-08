'use strict';
import React, { Component } from 'react';

import { Button, Modal } from 'antd';

import Charts from '../Charts';

import Storage from '../../../utils/storage';
import Generator from '../../../utils/generator';
import { getRadarOption } from '../../../utils/chart_option';

import 'whatwg-fetch';

export default class RadarChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: false,
      data: [],
      option: {},
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleClick() {
    this.setState({
      visible: true,
      data: [],
    });

    const _this = this;
    let postData = this.props.postData.id ? { id: this.props.postData.id } : { doc: this.props.postData.doc };

    fetch(`/api/mining/valuable`, {
      method: 'POST',
      credential: 'include',
      headers: {
        'Authorization': `Basic ${Storage.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(Object.assign(postData, {
        name_list: this.props.selection.toJS().map(item => { return item.id + '.md' }),
        uses: this.props.postData.uses,
      })),
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        _this.setState({
          data: json.data.result,
          option: getRadarOption(json.data.max, json.data.result),
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