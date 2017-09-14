'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';

import { getListProcessed, deleteMessage } from 'request/message';

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

  deleteListMessage = (key) => {
    const listprocessed = [...this.state.listprocessed];
    this.setState({ listprocessed: listprocessed.filter(item => item.id !== key) });
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
      title: '相关人',
      dataIndex: 'name',
    }, {
      title: '日期',
      dataIndex: 'date',
    }, {
      title: '相关公司',
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
          dataSource={this.state.listprocessed}
          loading={this.state.loading}
      />
    </div>
    );
  }
}

export default ProcessedMessage;
