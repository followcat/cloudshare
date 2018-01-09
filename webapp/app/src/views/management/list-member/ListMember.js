'use strict';
import React, { Component } from 'react';

import TablePlus from 'components/table-plus';
import ButtonWithModal from 'components/button-with-modal';
import ListMemberForm from 'components/project-list';

import {   message,Form,Table, Input,Button, Popconfirm } from 'antd';

import findIndex from 'lodash/findIndex';

import { getListMember, deleteMember, sendInviteMessage } from 'request/member';
import { elevateAdmin, revokeAdmin, } from 'request/memberadmin';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;


class ListMember extends Component {
	constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      members: [],
      visible: false,
      value: '',
      memberName: '',
    };
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleSubmit   = this.handleSubmit.bind(this);
    this.handleOkClick = this.handleOkClick.bind(this);
    this.getListMemberData = this.getListMemberData.bind(this);
    this.getMemberName = this.getMemberName.bind(this);
    this.handleElevate = this.handleElevate.bind(this);
    this.handleRevoke = this.handleRevoke.bind(this);
  }

  getListMemberData() {
    getListMember((json) => {
      if (json.code === 200) {
		    this.setState({
          members: json.result,
        });
      }
    });
  }

  getMemberName(childname){
    this.setState({ memberName: childname.name });
  }

  handleButtonClick() {
    this.setState({
      visible: true
    });
  }

  handleOkClick(){
     this.handleSubmit();
  }

  handleSubmit(feildValue) {
    sendInviteMessage({
      memberName: this.state.memberName,
    }, (json) => {
      if  (json.code === 200) {
        this.setState({
        visible: false
    });
      message.success(language.SENT_SUCCESS_MSG);
      } else {
        message.error(language.SENT_FAIL_MSG);
      }
    })
  }

  handleCancelClick() {
    this.setState({
      visible: false
    });
  }

  handleElevate(record) {
    elevateAdmin({
      userid: record.id,
    }, (json) => {
      if  (json.result === true) {
      this.getListMemberData();
      message.success(language.ELEVATE_SUCCESS);
      } else {
        message.error(language.ELEVATE_FAIL);
      }
    })
  }

  handleRevoke(record) {
    revokeAdmin({
      userid: record.id,
    }, (json) => {
      if  (json.result === true) {
      this.getListMemberData();
      message.success(language.REVOKE_SUCCESS);
      } else {
        message.error(language.REVOKE_FAIL);
      }
    })
  }

  getElements() {
    const elements = [{
      col: {
        span: 4
      },
      render: (
        <ButtonWithModal
          buttonStyle={{ marginLeft: 8 }}
          buttonType="primary"
          buttonText="邀请"
          visible={this.state.visible}
          modalTitle="邀请"
          modalOkText="提交"
          modalCancelText="取消"
          onButtonClick={this.handleButtonClick}
          onModalOk={this.handleOkClick}
          onModalCancel={this.handleCancelClick}
        >
        <ListMemberForm
              inputLabel="用户名称"
              getInput={this.getMemberName}
              onChange={this.handleFormChange}
              onSubmit={this.handleSubmit}
        />
        </ButtonWithModal>
      )
    }];

    return elements;
  }

  onDelete = (record) => {
    deleteMember({
      userid : record.id,
    }, (json) => {
      if  (json.result === true) {
      const members = [...this.state.members];
      this.setState({ members: members.filter(item => item.id !== record.id) });
      message.success(language.DELETE_SUCCESS_MSG);
      } else {
        message.error(language.DELETE_FAIL_MSG);
      }
    }) 
  }


  componentDidMount() {
    this.getListMemberData();
    }

  render() {
  	const columns = [{
      title: '成员名称',
      dataIndex: 'name',
  		render: text => <span>{text}</span>,
		},{
      title: '管理员',
      dataIndex: 'admin',
      render: (text, record) => {
        return (
        record.admin ?
        <span>{language.YES}</span>
        :
        <span>{language.NO}</span>
        )
      },
    },{
      title: '操作',
  		className: 'action',
  		dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.members.length > 0 ?
          ( 
            record.admin ? 
            (
            <span>
              <a href="#" onClick={() => this.handleRevoke(record)}>
              {language.REVOKE}
              <span className="ant-divider" /></a>
            <Popconfirm title="Sure to delete?" onConfirm={() => this.onDelete(record)}>
              <a href="#">{language.DELETE}</a>
            </Popconfirm>
            </span>
            ):
            (
              <span>
              <a href="#" onClick={() => this.handleElevate(record)}>
              {language.ELEVATE}
              <span className="ant-divider" /></a>
            <Popconfirm title="Sure to delete?" onConfirm={() => this.onDelete(record)}>
              <a href="#">{language.DELETE}</a>
            </Popconfirm>
            </span>
              )
          ) : null
        );
      },
		}];

  	const data = this.state.projects;
    return (
    <div className="cs-project-list">
      <TablePlus
          rowKey={record => record.id}
          isToolbarShowed={true}
          isSearched={true}
          elements={this.getElements()}
          columns={columns}
          dataSource={this.state.members}
          loading={this.state.loading}
      />
    </div>
    );
  }
}
export default ListMember;
