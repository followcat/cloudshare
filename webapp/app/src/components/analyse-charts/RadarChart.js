'use strict';
import React, { Component, PropTypes } from 'react';

import Charts from './Charts';

import { Button, Modal, Checkbox } from 'antd';

import { getValuableData } from 'request/analyse';

import { getRadarOption } from 'utils/chart_option';

class RadarChart extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      data: [],
      option: {},
      anonymized: false,
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleClick() {
    const { postData, selection } = this.props;

    this.setState({
      visible: true,
      data: [],
    });

    let param = postData.id ? { id: postData.id } : { doc: postData.doc };

    getValuableData(Object.assign(param, {
        name_list: selection.map(item => `${item.id}.md`),
        uses: postData.uses,
      }), json => {
        if (json.code === 200) {
          this.setState({
            data: json.data.result,
            option: getRadarOption(json.data.max, json.data.result, this.state.anonymized),
          });
        }
      });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  handleChange(e) {
    this.setState({
      anonymized: e.target.checked,
    });
  }

  render() {
    const { visible, option, data } = this.state;

    return (
      <div>
        <Button type="primary" onClick={this.handleClick}>显示雷达图</Button>
        <Checkbox onChange={this.handleChange}>匿名</Checkbox>
        <Modal
          title="图表"
          visible={visible}
          onCancel={this.handleCancel}
          footer={
            [<Button type="ghost" onClick={this.handleCancel}>关闭</Button>]
          }
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

RadarChart.propTypes = {
  postData: PropTypes.object,
  selection: PropTypes.array
};

export default RadarChart;
