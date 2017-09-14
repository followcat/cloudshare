'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';

import { getListRead, deleteMessage } from 'request/message';

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

  deleteListMessage = (key) => {
    const listread = [...this.state.listread];
    this.setState({ listread: listread.filter(item => item.id !== key) });
  }

  onDelete = (record) => {
    deleteMessage ({
      msgid : record.id
    }, (json) => {
      if (json.result === true) {
        this.deleteListMessage(record.id);
        message.success(language.SUCESS_MSG,1,function(){
        });
      } else {
        message.error(language.FAIL_MSG);
      }
    });
  }

  render() {
    const columns = [{
      title: '发送人',
      dataIndex: 'name',
    }, {
      title: '日期',
      dataIndex: 'date',
    }, {
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
            <Popconfirm title="删除信息?" onConfirm={() => this.onDelete(record)}>
              <a href="#">{language.DELETE}</a>
            </Popconfirm>
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
