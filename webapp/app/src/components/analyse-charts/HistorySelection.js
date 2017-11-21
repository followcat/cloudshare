'use strict';
import React, { Component, PropTypes } from 'react';

import { Button, Modal, Table } from 'antd';

import History from 'utils/history';

class HistorySelection extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      selectedRowKeys: [],
      data: []
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleSelectChange = this.handleSelectChange.bind(this);
  }

  handleClick() {
    const { selection } = this.props;

    const historyStorage = History.read();
    let selectData = [];

    historyStorage.forEach(item => {
      selection.forEach((value) => {
        if (item.id === value.id) {
          selectData.push(value.id);
        }
      });
    });
    this.setState({
      visible: true,
      data: historyStorage,
      selectedRowKeys: selectData
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  handleSelectChange(selectedRowKeys) {
    this.setState({
      selectedRowKeys: selectedRowKeys
    });
  }

  render() {
    const {
      selectedRowKeys,
      visible,
      data
    } = this.state;

    const columns = [
      {
        title: '简历ID',
        dataIndex: 'id',
        width: '40%',
        key: 'id',
      }, {
        title: '候选人名字',
        dataIndex: 'name',
        width: '50%',
        key: 'name',
      },
    ];

    const rowSelection = {
      type: 'checkbox',
      selectedRowKeys: selectedRowKeys,
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
        <Button type="primary" onClick={this.handleClick}>从浏览历史中选择</Button>
        <Modal
          title="浏览历史"
          visible={visible}
          onCancel={this.handleCancel}
          style={{ top: 40 }}
          footer={
            [<Button type="ghost" onClick={this.handleCancel}>取消</Button>]
          }
        >
          <Table
            columns={columns}
            dataSource={data}
            rowKey="id"
            rowSelection={rowSelection}
            size="small"
          />
        </Modal>
      </div>
    );
  }
}

HistorySelection.propTypes = {
  selection: PropTypes.array,
  onToggleSelection: PropTypes.func
};

export default HistorySelection;
