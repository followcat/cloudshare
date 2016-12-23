'use strict';
import React, { Component, PropTypes } from 'react';

import Header from '../../components/layout-header';

import { Modal, Menu } from 'antd';

import { URL } from '../../config/url';
import { signOut } from '../../request/sign';
import StorageUtil from '../../utils/storage';

import logo from '../../image/logo.png';
import websiteText from '../../config/website-text';

const language = websiteText.zhCN;

const MenuItem = Menu.Item,
      MenuDivider = Menu.Divider,
      confirm = Modal.confirm;


const navMenus = [{
  url: URL.getSearchURL(),
  text: language.SEARCH
}, {
  url: URL.getFastMatchingByDoc(),
  text: language.MATCH
}, {
  url: URL.getUploaderURL(),
  text: language.RESUME_UPLOADER
}, {
  url: URL.getProjectManagement(),
  text: language.PROJECT_MANAGEMENT
}];

class LayoutHeader extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: []
    };
    this.handleSignOutClick = this.handleSignOutClick.bind(this);
  }

  componentDidMount() {
    const href = location.href;
    let selectedKeys = [];

    navMenus.forEach(v => {
      if (href.indexOf(v.url) > -1) {
        selectedKeys.push(v.url);
      }
    });

    this.setState({
      selectedKeys: selectedKeys
    });
  }

  handleSignOutClick(e) {
    e.preventDefault();
    confirm({
      title: language.SIGN_OUT,
      content: language.SIGN_OUT_CONFIRM_MSG,
      onOk() {
        signOut((json) => {
          if (json.code === 200) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            location.href = json.redirect_url;
          }
        });
      },
      onCancel() {}
    });
  }

  render() {
    const { style, children } = this.props;

    const profileMenu = (
      <Menu>
        <MenuItem>
          <a href={URL.getUserInfoURL()}>{language.PROFILE}</a>
        </MenuItem>
        <MenuDivider />
        <MenuItem>
          <a
            href="#"
            onClick={this.handleSignOutClick}
          >
            {language.SIGN_OUT}
          </a>
        </MenuItem>
      </Menu>
    );

    return (
      <div style={style}>
        <Header
          logoImg={logo}
          navMenus={navMenus}
          profileMenu={profileMenu}
          project={StorageUtil.get('_pj')}
          profileText={StorageUtil.get('user')}
          selectedKeys={this.state.selectedKeys}
        />
        <div className="cs-layout-wrapper">
          {children}
        </div>
      </div>
    );
  }
}

LayoutHeader.propTypes = {
  style: PropTypes.object,
  children: PropTypes.element
};

export default LayoutHeader;
