'use strict';
import React, { Component } from 'react';

import Header from 'components/layout-header';

import { Modal, Menu, Badge  } from 'antd';

import { URL } from 'URL';

import { getProject } from 'request/project';
import { signOut } from 'request/sign';
import { isMember, isMemberAdmin } from 'request/member';

import StorageUtil from 'utils/storage';

import logo from 'image/logo.png';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

const MenuItem = Menu.Item,
      MenuDivider = Menu.Divider,
      confirm = Modal.confirm;

//member
const navMenusMember = [{
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
  text: language.VIP_MANAGEMENT
}, {
  url: URL.getBestExcellent(),
  text: language.BEST_EXCELLENT
}];
//account
const navMenuUser = [{
  url: URL.getSearchURL(),
  text: language.SEARCH
}, {
  url: URL.getFastMatchingByDoc(),
  text: language.MATCH
}, {
  url: URL.getUploaderURL(),
  text: language.RESUME_UPLOADER
}, {
  url: URL.getBecomeMember(),
  text: language.BECOME_MEMBER
}];

class LayoutHeader extends Component {
  constructor() {
    super();
    this.state = {
      selectedKeys: [],
      projects: [],
      navMenus: navMenuUser,
      profileMenus: [],
      ismember: '',
    };
    this.handleSignOutClick = this.handleSignOutClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentWillMount() {

    const profileMenuAdmin = ( 
    <Menu>
    <MenuItem>
      <a href={URL.getUserInfoURL()}>{language.PROFILE}</a>
    </MenuItem>
    <MenuDivider />
    <MenuItem>
      <a href={URL.getNotcieURL()}>{language.NOTICE}</a>
    </MenuItem>
    <MenuDivider />
    <MenuItem>
      <a href={URL.getManagement()}>{language.MANGEMENT}</a>
    </MenuItem>
    <MenuDivider />
    <MenuItem>
      <a href="#" onClick={this.handleSignOutClick}>
        {language.SIGN_OUT}
      </a>
    </MenuItem>
    </Menu>
    );

    const profileMenu = ( 
  <Menu>
    <MenuItem>
      <a href={URL.getUserInfoURL()}>{language.PROFILE}</a>
    </MenuItem>
    <MenuDivider />
    <MenuItem>
      <a href={URL.getNotcieURL()}>{language.NOTICE}</a>
    </MenuItem>
    <MenuDivider />
    <MenuItem>
      <a href="#" onClick={this.handleSignOutClick}>
        {language.SIGN_OUT}
      </a>
    </MenuItem>
  </Menu>
    );

      isMember((json) => {
      if (json.result === true) {
        this.setState({
          navMenus: navMenusMember,
          ismember: true,
        });
      }
      });
      isMemberAdmin((json) => {
      if (json.result === true) {
        this.setState({
          profileMenus: profileMenuAdmin,
        });
      } else{
          this.setState({
          profileMenus: profileMenu,
        });
        }
      });
      getProject((json) => {
      if (json.code === 200) {
        this.setState({
          projects: json.data,
        });
      }
    });
  }

  componentDidMount() {
    const href = location.href;
    let selectedKeys = [];

    this.state.navMenus.forEach(v => {
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

  render() {

    const { selectedKeys, projects, ismember, navMenus ,profileMenus } = this.state;
    return (
      <Header
        logoImg={logo}
        navMenus={navMenus}
        profileMenu={profileMenus}
        isMember={ismember}
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
