'use strict';
import React, { Component } from 'react';

import Navigation from 'components/navigation';
import Profile from 'components/manage/Profile';

import { Menu, Modal } from 'antd';

import { signOut } from 'request/sign';

import StorageUtil from 'utils/storage';
import { URL } from 'URL';

const MenuItem = Menu.Item,
      confirm = Modal.confirm;

export default class CommonNavigation extends Component {
  constructor() {
    super();
    this.getDropdownMenu = this.getDropdownMenu.bind(this);
    this.handleSignOutConfirm = this.handleSignOutConfirm.bind(this);
  }

  handleSignOutConfirm() {
    confirm({
      title: 'Sign out',
      content: 'Are you sure to sign out ?',
      onOk() {
        signOut((json) => {
          if (json.code === 200) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            location.href = json.redirect_url;
          }
        });
      },
      onCancel() {},
    });
  }

  getDropdownMenu() {
    return (
      <Menu>
        <Menu.Item key="0">
          <a href={URL.getUserInfoURL()}>Individual Center</a>
        </Menu.Item>
        <Menu.Divider />
        <MenuItem key="1">
          <a
            href="#"
            onClick={this.handleSignOutConfirm}
          >
            Sign out
          </a>
        </MenuItem>
      </Menu>
    );
  }

  render() {
    const navs = [{
      key: 'project',
      render: () => {
        return (
          <p style={{ color: '#fff' }}>{StorageUtil.get('_pj')}</p>
        );
      },
    }, {
      key: 'profile',
      render: () => {
        return (
          <Profile
            dropdownMenu={this.getDropdownMenu()}
            trigger={['click']}
            iconType="user"
            text={StorageUtil.get('user')}
          />
        );
      },
    }, {
      key: 'uploader',
      render: () => {
        return (
          <a
            href={URL.getUploaderURL()}
          >
            Uploader
          </a>
        );
      },
    }, {
      key: 'listjd',
      render: () => {
        return (
          <a
            href={URL.getListJDURL()}
          >
            JD List
          </a>
        );
      },
    }];

    return (
      <Navigation navs={navs} />
    );
  }
}
