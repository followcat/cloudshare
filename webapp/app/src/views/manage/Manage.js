'use strict';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import Header from 'components/header';
import Navigation from 'components/navigation';
import Viewport from 'components/viewport';
import Container from 'components/container';
import ShowCard from 'components/show-card';
import SiderMenu from 'components/sider-menu';
import Content from 'components/content';
import Profile from './Profile';

import { Menu, Modal } from 'antd';

import { getAccounts } from 'request/account';
import { signOut } from 'request/sign';

import { getCurrentActive } from 'utils/sider-menu-list';
import websiteText from 'config/website-text';

const language = websiteText.zhCN;
const MenuItem = Menu.Item,
      confirm = Modal.confirm;

class Manage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: getCurrentActive(props),
      dataSource: [],
      height: 0,
    };
    this.handleSignOutConfirm = this.handleSignOutConfirm.bind(this);
    this.getUserList = this.getUserList.bind(this);
  }

  componentDidMount() {
    this.getUserList();
    const eleShowCard = ReactDOM.findDOMNode(this.refs.showCard),
          height = eleShowCard.offsetHeight - 2*eleShowCard.offsetTop - 44;

    this.setState({
      height: height,
    });
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.location.pathname !== this.props.location.pathname) {
      this.setState({
        current: getCurrentActive(this.props, nextProps),
      });
    }
  }

  handleSignOutConfirm() {
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
      onCancel() {},
    });
  }
  
  getUserList() {
    getAccounts((json) => {
      if (json.code === 200) {
        let datas = json.data.map((value, index) => {
          return { key: index, name: value };
        });
        this.setState({
          dataSource: datas,
        });
      }
    });
  }

  render() {
    const dropdownMenu = (
      <Menu>
        <MenuItem key="0">
          <a href="#" onClick={this.handleSignOutConfirm}>登出</a>
        </MenuItem>
      </Menu>
    );

    const navs = [{
      key: 'profile',
      render: () => {
        return (
          <Profile 
            dropdownMenu={dropdownMenu}
            trigger={['click']}
            iconType="user"
            text={localStorage.user}
          />
        );
      },
    }];

    const menus = [{
      key: 'users',
      url: '/manage/users',
      text: '用户列表'
    }, {
      key: 'setting',
      url: '/manage/setting',
      text: '设置'
    }];

    return (
      <Viewport>
        <Header fixed={true}>
          <Navigation navs={navs} />
        </Header>
        <Container className="cs-layout-manage">
          <ShowCard ref="showCard">
            <SiderMenu
              selectedKeys={[this.state.current]}
              menus={menus}
            />
            <Content>
              {this.props.children && React.cloneElement(this.props.children, {
                dataSource: this.state.dataSource,
                height: this.state.height,
                getUserList: this.getUserList,
                style: { paddingTop: 40 }
              })}
            </Content>
          </ShowCard>
        </Container>
      </Viewport>
    );
  }
}

export default Manage;
