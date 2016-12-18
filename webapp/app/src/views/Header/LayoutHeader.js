'use strict';
import React, { Component } from 'react';

import Header from '../../components/layout-header';

import { Menu } from 'antd';

import { URL } from '../../config/url';
import StorageUtil from '../../utils/storage';
import logo from '../../image/logo.png';

import websiteText from '../../config/website-text';

const language = websiteText.zhCN;

const MenuItem = Menu.Item,
      MenuDivider = Menu.Divider;


export default class LayoutHeader extends Component {
  constructor() {
    super();
    this.getDefaultSelectedKeys = this.getDefaultSelectedKeys.bind(this);
  }

  getDefaultSelectedKeys(navMenus) {
    const href = location.href;
    let defaultSelectedKeys = [];

    navMenus.forEach(v => {
      if (href.indexOf(v.url) > 0) {
        defaultSelectedKeys.push(v.url);
      }
    });
    
    return defaultSelectedKeys;
  }

  render() {
    const { style, children } = this.props;

    const navMenus = [{
      url: URL.getSearchURL(),
      text: language.SEARCH
    }, {
      url: URL.getFastMatching(),
      text: language.MATCH
    }, {
      url: URL.getProjectManagement(),
      text: language.PROJECT_MANAGEMENT
    }];

    const profileMenu = (
      <Menu>
        <MenuItem>
          <a href={URL.getUserInfoURL()}>{language.PROFILE}</a>
        </MenuItem>
        <MenuDivider />
        <MenuItem>
          <a href="#">{language.SIGN_OUT}</a>
        </MenuItem>
      </Menu>
    );

    const defaultSelectedKeys = this.getDefaultSelectedKeys(navMenus);

    return (
      <div style={style}>
        <Header
          logoImg={logo}
          navMenus={navMenus}
          profileMenu={profileMenu}
          profileText={StorageUtil.get('user')}
          defaultSelectedKeys={defaultSelectedKeys}
        />
        <div className="cs-layout-wrapper">
          {children}
        </div>
      </div>
    );
  }
}