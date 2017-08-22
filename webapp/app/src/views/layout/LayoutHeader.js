'use strict';
import React, { Component } from 'react';

import Header from 'components/layout-header';

import { Modal, Menu } from 'antd';

import { URL } from 'URL';

import { getProject } from 'request/project';
import { signOut } from 'request/sign';
import StorageUtil from 'utils/storage';

import logo from '../../image/logo.png';

import websiteText from 'config/website-text';

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
}, {
  url: URL.getBestExcellent(),
  text: language.BEST_EXCELLENT
}];

class LayoutHeader extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: []
    };
    this.handleSignOutClick = this.handleSignOutClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    const href = location.href;
    let selectedKeys = [];
    
    this.getProjectData();

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
             localStorage.clear();
            location.href = json.redirect_url;
          }
        });
      },
      onCancel() {}
    });
  }

  handleChange(value) {
    StorageUtil.set('_pj', value);
    window.location.reload();
  }

  getProjectData() {
    getProject((json) => {
      if (json.code === 200) {
        this.setState({
          projects: json.data,
        });
      }
    });
  }

  render() {
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

    const { selectedKeys, projects } = this.state;

    return (
      <Header
        logoImg={logo}
        navMenus={navMenus}
        profileMenu={profileMenu}
        projects={projects}
        project={StorageUtil.get('_pj')}
        profileText={StorageUtil.get('user')}
        selectedKeys={selectedKeys}
        onChange={this.handleChange}
      />
    );
  }
}

export default LayoutHeader;
