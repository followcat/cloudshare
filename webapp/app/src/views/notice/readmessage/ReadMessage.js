'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';

import { getListRead } from 'request/message';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;

class ReadMessage extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      visible: false,
      value: '',
      listread: [],
    };
  }  

  getReadMsg() {
    getListRead ((json) => {
      if (json.code === 200) {
        this.setState({
          listread: json.result,
        });
      }
    });
  }

  componentDidMount() {
    this.getReadMsg();
    }

  render() {
    const columns = [{
      title: '日期',
      dataIndex: 'date',
    },{
      title: '内容',
      dataIndex: 'content',
      render: text => <span>{text}</span>,
    }, {
     title: '操作',
      className: 'action',
      dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.listread.length > 0 ?
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
          dataSource={this.state.listread}
          loading={this.state.loading}
      />
    </div>
    );
  }
}

export default ReadMessage;
