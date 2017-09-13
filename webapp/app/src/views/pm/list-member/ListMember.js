'use strict';
import React, { Component } from 'react';

import TablePlus from 'components/table-plus';
import ButtonWithModal from 'components/button-with-modal';
import ListCustomerForm from 'components/project-list';

import {   message, Form, Table, Input, Button, Popconfirm } from 'antd';

import findIndex from 'lodash/findIndex';

import { getListMenber, deleteMenber, sendInviteMessage } from 'request/member';
import { elevateAdmin,  } from 'request/memberadmin';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;


class ListMember extends Component {
	constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      customers: [],
      visible: false,
      value: '',
      customerName: '',
    };
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleSubmit   = this.handleSubmit.bind(this);
    this.handleOkClick = this.handleOkClick.bind(this);
    this.getListMenberData = this.getListMenberData.bind(this);
    this.getMenberName = this.getMenberName.bind(this);
    this.handleElevate = this.handleElevate.bind(this);
  }

  getListMemberData() {
    getListMember((json) => {
      if (json.code === 200) {
		    this.setState({
          customers: json.result,
        });
      }
    });
  }

  getMemberName(childname){
    this.setState({ customerName: childname.name });
  }

  handleButtonClick() {
    this.setState({
      visible: true
    });
  }

  handleOkClick(){
     this.handleSubmit();
  }

  handleSubmit (feildValue) {
    sendInviteMessage({
      customerName: this.state.customerName,
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
    },(json) => {
      if (json.result === true) {
      message.success(language.SENT_SUCCESS_MSG);
      } else {
        message.error(language.SENT_FAIL_MSG);
      }
    });
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
        <ListCustomerForm
              inputLabel="用户名称"
              getInput={this.getCustomerName}
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
      if  (json.code === 200) {
      const customers = [...this.state.customers];
      this.setState({ customers: customers.filter(item => item.id !== record.id) });
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
		}, {
      title: '操作',
  		className: 'action',
  		dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.customers.length > 0 ?
          (
            <span>
            <a href="#" onClick={() => this.handleElevate(record)}>{language.ELEVATE}</a>
            <span className="ant-divider" />
            <a href="#"onClick={() => this.handleRevoke(record)}>{language.REVOKE}</a>
            <span className="ant-divider" />
            <Popconfirm title="Sure to delete?" onConfirm={() => this.onDelete(record)}>
              <a href="#">{language.DELETE}</a>
            </Popconfirm>
            </span>
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
          dataSource={this.state.customers}
          loading={this.state.loading}
      />
    </div>
    );
  }
}
export default ListMember;
