'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';
import inviteMsg from 'components/invite-message';

import { getListInvited,readMessage,acceptInviteMessage } from 'request/message';

import { URL } from 'URL';
import websiteText from 'config/website-text';
const language = websiteText.zhCN;

class InviteMessage extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      visible: false,
      value: '',
      listinvited: [],
    };
  }  

  getInviteMsg() {
    getListInvited ((json) => {
      if (json.code === 200) {
        this.setState({
          listinvited: json.result,
        });
      }
    });
  }

  onIgnore = (key) =>{
    acceptInviteMessage ({
        msgid : key,
       reply : false,
    }, (json) => {
      if (json.code === 200) {
          this.onDelete(key);
      } 
    });
  }


  onDelete = (key) => {
    const listinvited = [...this.state.listinvited];
    this.setState({ listinvited: listinvited.filter(item => item.id !== key) });
  }

  onAccept = (record) => {
    acceptInviteMessage ({
        msgid : record.id,
       reply : true,
    }, (json) => {
      if (json.result === true) {
        this.onDelete(record.id);
        message.success(language.ACCEPT_INVITE_SUCCESS_MSG);
      } else {
        message.error(language.ACCEPT_INVITE_FAIL_MSG);
      }
    });
  }

  componentDidMount() {
    this.getInviteMsg();
    }

  render() {
    const columns = [{
      title: 'companyName',
      dataIndex: 'content',
      render: text => <a href="#">{text}</a>,
    }, {
      title: 'date',
      dataIndex: 'date',
    }, {
     title: 'action',
      className: 'action',
      dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.listinvited.length > 0 ?
          ( 
            <span>
            <a href="#" onClick={() => this.onAccept(record)}>accept</a>
            <span className="ant-divider" />
            <Popconfirm title="Sure to delete?" onConfirm={() => this.onIgnore(record.id)}>
              <a href="#">ignore</a>
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
          isSearched={true}
          columns={columns}
          rowKey={record => record.id}
          dataSource={this.state.listinvited}
          loading={this.state.loading}
      />
    </div>
    );
  }
}

export default InviteMessage;
