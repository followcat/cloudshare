'use strict';
import React, { Component } from 'react';

import { Menu, Dropdown, Icon, Modal, message } from 'antd';

import LogoImg from '../../image/logo.png';

import config from '../../../config';

export default class Header extends Component {
  constructor() {
    super();
    this.handleShowConfirm = this.handleShowConfirm.bind(this);
  }

  handleShowConfirm() {
    fetch(`${config.host}/api/session`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Basic ${localStorage.token}`
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
  }

  render() {
    const menu = (
      <Menu>
        <Menu.Item key="0">
          <a href="#" onClick={this.handleShowConfirm}>Sign out</a>
        </Menu.Item>
      </Menu>
    );
    return (
      <div className="cs-layout-top">
        <div className="cs-layout-herader">
          <div className="cs-layout-wrapper">
            <div className="cs-layout-logo">
              <img src={LogoImg} alt="Logo" />
            </div>
            <div className="cs-layout-person">
              <Dropdown overlay={menu} trigger={['click']}>
                <a className="ant-dropdown-link" href="#">
                  <Icon type="user" />{localStorage.user} <Icon type="down" />
                </a>
              </Dropdown>
            </div>
          </div>
        </div>
      </div>
    );
  }
}