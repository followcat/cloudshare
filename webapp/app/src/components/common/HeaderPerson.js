'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';
import { Menu, Dropdown, Icon, Modal, message } from 'antd';

export default class HeaderPerson extends Component {
  constructor() {
    super();
    this.handleShowConfirm = this.handleShowConfirm.bind(this);
  }

  handleShowConfirm() {
    Modal.confirm({
      title: 'Sign out',
      content: 'Are yout sure to sign out?',
      wrapClassName: 'vertical-center-modal',
      onOk() {
        fetch(`/api/session`, {
          method: 'DELETE',
          credentials: 'include',
          headers: {
            'Authorization': `Basic ${localStorage.token}`,
          },
        })
        .then((response) => {
          return response.json();
        })
        .then((json) => {
          if (json.code === 200) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            location.href = json.redirect_url;
          } else {
            message.error(json.message);
          }
        });
      },
      onCancel() {},
    });
  }

  render() {
    const menu = (
      <Menu>
        <Menu.Item key="0">
          <a href="http://www.alipay.com/">Individual Center</a>
        </Menu.Item>
        <Menu.Divider />
        <Menu.Item key="1">
          <a href="#" onClick={this.handleShowConfirm}>Sign out</a>
        </Menu.Item>
      </Menu>
    );
    return (
      <div>
        <Dropdown overlay={menu} trigger={['click']}>
          <a className="ant-dropdown-link" href="#">
            <Icon type="user" />{localStorage.user} <Icon type="down" />
          </a>
        </Dropdown>
      </div>
    );
  }
}