'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';

import { getListUnread } from 'request/message';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;

class UnreadMessage extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      visible: false,
      value: '',
      listunread: [],
    };
  }  

  getUnreadMsg() {
    getListUnread ((json) => {
      if (json.code === 200) {
        this.setState({
          listunread: json.result,
        });
      }
    });
  }

  componentDidMount() {
    this.getUnreadMsg();
    }

  render() {
    const columns = [{
      title: '日期',
      dataIndex: 'date',
    }{
      title: '内容',
      dataIndex: 'content',
      render: text => <span>{text}</span>,
    },, {
     title: '操作',
      className: 'action',
      dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.listunread.length > 0 ?
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
          dataSource={this.state.listunread}
          loading={this.state.loading}
      />
    </div>
    );
  }
}

export default UnreadMessage;
