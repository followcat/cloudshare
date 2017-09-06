'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col ,Popconfirm,message } from 'antd';

import TablePlus from 'components/table-plus';
import inviteMsg from 'components/invite-message';

import { getListInvited } from 'request/message';
import { acceptInviteMessage } from 'request/customer';

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
        var jsontest = [];
        var fin = [];
    // json.data.map((item,index) => { return jsontest.push('{"key"'+':"'+index+'",'+'projectname'+':"'+item+'"}') });
    // jsontest.map((item,index) => { return fin.push(eval('(' + item + ')')) });
        this.setState({
          listinvited: json.result,
        });
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
       userid : record.relation,
        name : record.content,
    }, (json) => {
      if (json.code === 200) {
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
            <Popconfirm title="Sure to delete?" onConfirm={() => this.onDelete(record.id)}>
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
