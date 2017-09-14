'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';

import { getListInvited, readMessage, acceptInviteMessage } from 'request/message';

import websiteText from 'config/website-text';
import StorageUtil from '../../../utils/storage';

const language = websiteText.zhCN;

class InvitedMessage extends Component {
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
        StorageUtil.unset('_pj');
        this.onDelete(record.id);
        message.success(language.ACCEPT_INVITE_SUCCESS_MSG,1,function(){
        window.location.reload();  
        });
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
      title: '邀请人',
      dataIndex: 'name',
    }, {
      title: '日期',
      dataIndex: 'date',
    }, {
      title: '邀请公司',
      dataIndex: 'content',
      render: text => <span>{text}</span>,
    }, {
     title: '操作',
      className: 'action',
      dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.listinvited.length > 0 ?
          ( 
            <span>
            <a href="#" onClick={() => this.onAccept(record)}>{language.ACCEPT}</a>
            <span className="ant-divider" />
            <Popconfirm title="拒绝邀请?" onConfirm={() => this.onIgnore(record.id)}>
              <a href="#">{language.REJECT}</a>
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
          dataSource={this.state.listinvited}
          loading={this.state.loading}
      />
    </div>
    );
  }
}

export default InvitedMessage;
