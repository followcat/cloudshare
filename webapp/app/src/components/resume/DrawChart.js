'use strict';
import React, { Component, PropTypes } from 'react';

import { Modal, Button, Collapse, Table, Input } from 'antd';

import Charts from '../common/Charts';

export default class DrawChart extends Component {

  constructor(props) {
    super(props);

    this.state = {
      visible: false,
      jdId: '',
      jdDoc: '',
      type: 'id',
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCollapseChange = this.handleCollapseChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleClick() {
    this.setState({
      visible: true,
    });
    this.props.onDrawChartOpen();
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  handleCollapseChange(e) {
    this.setState({
      type: e
    });
  }

  handleInputChange(event) {
    this.setState({
      jdDoc: event.target.value,
    });
  }

  handleSubmit() {
    let value = this.state.type === 'id' ? this.state.jdId : this.state.jdDoc,
        object = { type: this.state.type, value: value };
    this.props.onDrawChartSubmit(object);
  }

  render() {

    const columns = [
      {
        title: 'Company Name',
        dataIndex: 'company',
        key: 'company',
        width: 120,
      }, {
        title: 'Position',
        dataIndex: 'name',
        key: 'position',
        width: 360,
      }, {
        title: 'Creator',
        dataIndex: 'committer',
        key: 'creator',
      }
    ];

    const rowSelection = {
      type: 'radio',
      onChange: (selectedRowKeys, selectedRows) => {
        this.setState({
          jdId: selectedRows[0].id,
        });
      },
    };

    const pagination = {
      total: this.props.jdList.length,
      pageSize: 5,
      size: 'small',
    };

    return (
      <div style={this.props.style}>
        <Button
          type="ghost"
          size="small"
          onClick={this.handleClick}
        >
          Draw Chart
        </Button>
        <Modal
          title="Draw Chart"
          visible={this.state.visible}
          style={{ top: 12 }}
          width={720}
          onCancel={this.handleCancel}
        >
          <Collapse
            accordion
            defaultActiveKey="id"
            onChange={this.handleCollapseChange}
          >
            <Collapse.Panel
              header={'Job description list'}
              key="id"
            >
              <Table
                columns={columns}
                dataSource={this.props.jdList}
                rowSelection={rowSelection}
                pagination={pagination}
                size="small"
              />
            </Collapse.Panel>
            <Collapse.Panel
              header={'Job description document'}
              key="doc"
            >
              <Input
                type="textarea"
                rows="4"
                onChange={this.handleInputChange}
              />
            </Collapse.Panel>
          </Collapse>
          <Button
            type="ghost"
            style={{ marginTop: 4 }}
            onClick={this.handleSubmit}
          >
            Submit
          </Button>
          {Object.keys(this.props.radarOption).length > 0 ?
            <Charts
              option={this.props.radarOption}
              style={{ width: '100%', height: 460, marginTop: 10 }}
            />
           : ''}
        </Modal>
      </div>
    );
  }
}