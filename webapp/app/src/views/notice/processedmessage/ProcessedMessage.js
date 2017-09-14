'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';

import { getListProcessed } from 'request/message';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;

class ProcessedMessage extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      visible: false,
      value: '',
      listprocessed: [],
    };
  }  

  getProcessedMsg() {
    getListProcessed ((json) => {
      if (json.code === 200) {
        this.setState({
          listprocessed: json.result,
        });
      }
    });
  }

  componentDidMount() {
    this.getProcessedMsg();
    }

  render() {
    const columns = [{
      title: '日期',
      dataIndex: 'date',
    },{
      title: '邀请公司',
      dataIndex: 'content',
      render: text => <span>{text}</span>,
    }, {
     title: '操作',
      className: 'action',
      dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.listprocessed.length > 0 ?
          ( 
            <span>
            </span>
          ) : null
        );
      },
    }];

    const {
      storage,
      title,
      bordered,
      bodyStyle
    } = this.props;

    return (
      <div className="cs-InviteMessage">
      <TablePlus
          isToolbarShowed={true}
          columns={columns}
          rowKey={record => record.id}
          dataSource={this.state.listprocessed}
          loading={this.state.loading}
      />
    </div>
    );
  }
}

export default ProcessedMessage;
