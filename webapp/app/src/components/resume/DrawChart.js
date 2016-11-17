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
      selectedRowKeys: [],
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCollapseChange = this.handleCollapseChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleOk = this.handleOk.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleRowSelectionChange = this.handleRowSelectionChange.bind(this);
    this.handlePaginationChange = this.handlePaginationChange.bind(this);
    this.handleRowSelectionSelect = this.handleRowSelectionSelect.bind(this);
  }

  handleClick() {
    this.setState({
      visible: true,
    });
    this.props.onDrawChartOpen();
  }

  handleOk() {
    this.setState({
      visible: false,
    });
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

  handleRowSelectionChange(selectedRowKeys, selectedRows) {
    this.setState({
      selectedRowKeys: selectedRowKeys,
    });
  }

  handlePaginationChange() {
    this.setState({
      selectedRowKeys: [],
      jdId: '',
    });
  }

  handleRowSelectionSelect(record, selected, selectedRows) {
    this.setState({
      jdId: record.id,
    });
  }

  render() {

    const columns = [
      {
        title: 'Company Name',
        dataIndex: 'company_name',
        key: 'company_name',
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
      selectedRowKeys: this.state.selectedRowKeys,
      onChange: this.handleRowSelectionChange,
      onSelect: this.handleRowSelectionSelect,
    };

    const pagination = {
      total: this.props.jdList.length,
      pageSize: 5,
      size: 'small',
      onChange: this.handlePaginationChange
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
          width={980}
          onOk={this.handleOk}
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