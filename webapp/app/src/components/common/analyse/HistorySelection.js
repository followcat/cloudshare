'use strict';
import React, { Component } from 'react';

import { Button, Modal, Table } from 'antd';

import History from '../../../utils/history';

export default class HistorySelection extends Component {
  
  constructor() {
    super();

    this.state = {
      visible: false,
      selectedRowKeys: [],
      data: [],
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleSelectChange = this.handleSelectChange.bind(this);
  }

  handleClick() {
    const historyStorage = History.read(),
          selection = this.props.selection;
    let selectData = [];

    historyStorage.forEach((item, index) => {
      selection.forEach((value) => {
        if (item.id === value.get('id')) {
          selectData.push(index);
        }
      });
    });
    this.setState({
      visible: true,
      data: historyStorage,
      selectedRowKeys: selectData,
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  handleSelectChange(selectedRowKeys) {
    this.setState({
      selectedRowKeys: selectedRowKeys,
    });
  }

  render() {
    const columns = [
      {
        title: 'Resume ID',
        dataIndex: 'id',
        width: '30%',
        key: 'id',
      }, {
        title: 'Name',
        dataIndex: 'name',
        width: '50%',
        key: 'name',
      },
    ];

    const rowSelection = {
      type: 'checkbox',
      selectedRowKeys: this.state.selectedRowKeys,
      onChange: this.handleSelectChange,
      onSelect: (record) => {
        this.props.onToggleSelection({
          id: record.id,
          name: record.name
        });
      },
    };

    return (
      <div>
        <Button type="primary" onClick={this.handleClick}>Select From History</Button>
        <Modal
          title="Browsing History"
          visible={this.state.visible}
          onCancel={this.handleCancel}
          style={{ top: 40 }}
          footer={
            [<Button type="ghost" onClick={this.handleCancel}>Cancel</Button>]
          }
        >
          <Table 
            columns={columns}
            dataSource={this.state.data}
            rowSelection={rowSelection}
            size="small"
          />
        </Modal>
      </div>
    );
  }
}