'use strict';
import React, { Component, PropTypes } from 'react';

import Charts from './Charts';

import { Button, Modal, Checkbox, Spin } from 'antd';

import { getValuableData } from 'request/analyse';

import { getRadarOption } from 'utils/chart_option';

class RadarChart extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      data: [],
      option: {},
      defaultSelection: [],
      anonymized: false,
      spinning: true
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleLoading = this.handleLoading.bind(this);
  }

  handleClick() {
    const { postData, selection, dataSource, } = this.props;
    let defaultSelection = selection ? selection : [];
    this.setState({
      visible: true,
      spinning: true,
      data: [],
    });

    let param = postData.id ? { id: postData.id } : { doc: postData.doc };
    if (dataSource.length > 0 && selection.length <= 0) {
       defaultSelection = [];
       for (var i = 0; i < 3; i++) {
        defaultSelection.push({
          id: dataSource[i].yaml_info.id,
          name: dataSource[i].yaml_info.name
        })
       }
    }

    getValuableData(Object.assign(param, {
        name_list: defaultSelection.map(item => `${item.id}`),
        uses: postData.uses,
      }), json => {
        if (json.code === 200) {
          this.setState({
            data: json.data.result,
            option: getRadarOption(json.data.max, json.data.result, this.state.anonymized),
            spinning: false
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

  handleLoading(val) {
    this.setState({
      loading: val
    });
  }

  render() {
    const { visible, option, data, spinning } = this.state;

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
        <Spin spinning={spinning}>
          {data.length > 0 ?
            <Charts option={option} getLoading={this.handleLoading} 
            style={{ width: 900, height: 460, margin: '0 auto' }} />
            : <div style={{ width: 900, height: 460, margin: '0 auto' }} />
          }
          </Spin>
        </Modal>
      </div>
    );
  }
}

RadarChart.propTypes = {
  postData: PropTypes.object,
  selection: PropTypes.array,
  onClick: PropTypes.func
};

export default RadarChart;
