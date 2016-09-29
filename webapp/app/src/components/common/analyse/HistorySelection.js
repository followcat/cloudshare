'use strict';
import React, { Component } from 'react';

import { Button, Modal, Table } from 'antd';

export default class HistorySelection extends Component {
  
  constructor() {
    super();

    this.state = {
      visible: false,
      data: [],
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleClick() {
    this.setState({
      visible: true,
      data: JSON.parse(localStorage.history),
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  render() {
    const columns = [
      {
        title: 'Resume ID',
        dataIndex: 'id',
        width: '30%',
      }, {
        title: 'Name',
        dataIndex: 'name',
        width: '50%',
      },
    ];

    const rowSelection = {
      type: 'checkbox',
      getCheckboxProps: record => ({
        defaultChecked: this.props.selection.findIndex(v => v.get('id') === record.id ) > -1 ? true : false,
      }),
      onSelect: (record, selected, selectedRows) => {
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