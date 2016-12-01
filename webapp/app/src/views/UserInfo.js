'use strict';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Viewport from '../components/viewport';
import Header from '../components/header';
import CommonNavigation from './CommonNavigation';
import ShowCard from '../components/show-card';
import Container from '../components/container';
import SiderMenu from '../components/sider-menu';
import Content from '../components/content';
import { message, Popconfirm } from 'antd';
import { getBookmark, deleteBookmark } from '../request/bookmark';
import { resetPassword } from '../request/password';
import { signOut } from '../request/sign';
import { URL } from '../config/url';
import { getMenu, getCurrentActive } from '../utils/sider-menu-list';
import History from '../utils/history';
import './user-info.less';

export default class UserInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: getCurrentActive(props),
      storage: [],
      bookmarkList: [],
      historyHeight: 0,
      bookmarkHeight: 0,
    };
    this.handleDeleteConfirm = this.handleDeleteConfirm.bind(this);
    this.handleChangePasswordSubmit = this.handleChangePasswordSubmit.bind(this);
    this.getStorage = this.getStorage.bind(this);
    this.getBookmarkList = this.getBookmarkList.bind(this);
    this.getColumns = this.getColumns.bind(this);
  }

  componentDidMount() {
    this.getStorage();
    this.getBookmarkList();
    const eleShowCard = ReactDOM.findDOMNode(this.refs.showCard),
          historyBoxHeight = eleShowCard.offsetHeight - 2*eleShowCard.offsetTop - 48,
          bookmarkBoxHeight = eleShowCard.offsetHeight - 2*eleShowCard.offsetTop - 169;

    this.setState({
      historyHeight: historyBoxHeight,
      bookmarkHeight: bookmarkBoxHeight,
    });
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.location.pathname !== this.props.location.pathname) {
      this.setState({
        current: getCurrentActive(this.props, nextProps),
      });
    }
  }

  handleDeleteConfirm(bookmarkId) {
    deleteBookmark({
      bookmark_id: bookmarkId,
    }, (json) => {
      if (json.code === 200) {
        this.getBookmarkList();
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  handleChangePasswordSubmit(value) {
    const params = {
      oldpassword: value.oldPassword,
      newpassword: value.reNewPassword,
    };

    resetPassword(params, (json) => {
      if (json.code === 200) {
        message.success(json.message);
        setTimeout(() => {
          signOut((response) => {
            if (response.code === 200) {
              localStorage.removeItem('token');
              localStorage.removeItem('user');
              location.href = response.redirect_url;
            }
          });
        }, 1000);
      } else {
        message.error(json.message);
      }
    });
  }

  getStorage() {
    const storage = History.read();
    this.setState({
      storage: storage,
    });
  }

  getBookmarkList() {
    getBookmark((json) => {
      if (json.code === 200) {
        this.setState({
          bookmarkList: json.data,
        });
      }
    });
  }

  getColumns() {
    const columns = [{
      title: 'Name',
      dataIndex: 'name',
      width: 150,
      key: 'name',
      render: (text, record) => (
        <a href={URL.getResumeURL(record.id)}>
          {text || record.id}
        </a>
      )
    }, {
      title: 'Gender',
      dataIndex: 'gender',
      width: 120,
      key: 'gender',
    }, {
      title: 'Age',
      dataIndex: 'age',
      width: 120,
      key: 'age',
    }, {
      title: 'Position',
      dataIndex: 'position',
      key: 'position',
      width: 240,
    }, {
      title: 'Operation',
      key: 'operation',
      render: (text, record) => (
        <Popconfirm
          title="Are you sure to delete this bookmark?"
          placement="left"
          onConfirm={() => this.handleDeleteConfirm(record.id)}
        >
          <a href="#">Delete</a>
        </Popconfirm>
      ),
    }];

    return columns;
  }

  render() {
    return (
      <Viewport>
        <Header 
          fixed={true}
          logoLink={URL.getSearchURL()}
        >
          <CommonNavigation />
        </Header>
        <Container>
          <ShowCard ref="showCard">
            <SiderMenu
              selectedKeys={[this.state.current]}
              menus={getMenu(this.props.route.childRoutes)}
            />
            <Content>
              {this.props.children && React.cloneElement(this.props.children, {
                storage: this.state.storage,
                bodyStyle: {
                  height: this.state.historyHeight,
                  overflowY: 'scroll',
                },
                scroll: { y: this.state.bookmarkHeight },
                columns: this.getColumns(),
                bookmarkList: this.state.bookmarkList,
                settingPrefixCls: 'cs-setting',
                onSubmit: this.handleChangePasswordSubmit
              })}
            </Content>
          </ShowCard>
        </Container>
      </Viewport>
    );
  }
}
