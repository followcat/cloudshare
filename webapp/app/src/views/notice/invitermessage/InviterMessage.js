'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';

import { getListInviter } from 'request/message';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;

class InviterMessage extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      visible: false,
      value: '',
      listinviter: [],
    };
  }  

  getInviterMsg() {
    getListInviter ((json) => {
      if (json.code === 200) {
        this.setState({
          listinviter: json.result,
        });
      }
    });
  }

  componentDidMount() {
    this.getInviterMsg();
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
          this.state.listinviter.length > 0 ?
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
          dataSource={this.state.listinviter}
          loading={this.state.loading}
      />
    </div>
    );
  }
}

export default InviterMessage;
