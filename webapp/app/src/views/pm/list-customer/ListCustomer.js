'use strict';
import React, { Component } from 'react';

import TablePlus from 'components/table-plus';
import ButtonWithModal from 'components/button-with-modal';
import ListCustomerForm from 'components/project-list';

import {   message,Form,Table, Input,Button, Popconfirm } from 'antd';

import findIndex from 'lodash/findIndex';

import { getListCustomer,sendInviteMessage } from 'request/customer';

import websiteText from 'config/website-text';
const language = websiteText.zhCN;


class ListCustomer extends Component {
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
    this.getListCustomerData = this.getListCustomerData.bind(this);
    this.getCustomerName = this.getCustomerName.bind(this);
  }

  getListCustomerData() {
    getListCustomer((json) => {
      if (json.code === 200) {
		    var jsontest = [];
		    var fin = [];
		    json.result.map(item => item.inviter).map((item,index) => { return jsontest.push('{"key"'+':"'+index+'",'+'customername'+':"'+item+'"}') });
		    jsontest.map((item,index) => { return fin.push(eval('(' + item + ')')) });
		    this.setState({
          customers: fin,
        });
      }
    });
  }

  getCustomerName(childname){
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
      customerName: this.state.customerName || feildValue.customerName,
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

  onDelete = (key) => {
    const customers = [...this.state.customers];
    this.setState({ customers: customers.filter(item => item.key !== key) });
  }


  componentDidMount() {
    this.getListCustomerData();
    }

  render() {
  	const columns = [{
  		title: 'customerName',
  		dataIndex: 'customername',
  		render: text => <a href="#">{text}</a>,
		}, {
 		 title: 'action',
  		className: 'action',
  		dataIndex: 'action',
      render: (text, record) => {
        return (
          this.state.customers.length > 1 ?
          (
            <Popconfirm title="Sure to delete?" onConfirm={() => this.onDelete(record.key)}>
              <a href="#">delete</a>
            </Popconfirm>
          ) : null
        );
      },
		}];

  	const data = this.state.projects;
    return (
    <div className="cs-project-list">
      <TablePlus
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
export default ListCustomer;