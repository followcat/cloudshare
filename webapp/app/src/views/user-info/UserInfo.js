'use strict';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import ShowCard from 'components/show-card';
import Container from 'components/container';
import SiderMenu from 'components/sider-menu';
import Content from 'components/content';
import { Layout } from 'views/layout';

import { message, Popconfirm } from 'antd';

import { getBookmark, deleteBookmark } from 'request/bookmark';
import { resetPassword } from 'request/password';
import { signOut } from 'request/sign';

import { URL } from 'URL';

import { getCurrentActive } from 'utils/sider-menu-list';
import History from 'utils/history';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

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
      title: '候选人姓名',
      dataIndex: 'name',
      width: 150,
      key: 'name',
      render: (text, record) => (
        <a href={URL.getResumeURL(record.id)} target="_blank">{text || record.id}</a>
      )
    }, {
      title: '性别',
      dataIndex: 'gender',
      width: 120,
      key: 'gender',
    }, {
      title: '年龄',
      dataIndex: 'age',
      width: 120,
      key: 'age',
    }, {
      title: '职位',
      dataIndex: 'position',
      key: 'position',
      width: 240,
    }, {
      title: '操作',
      key: 'operation',
      render: (text, record) => (
        <Popconfirm
          title="确定进行删除操作?"
          placement="left"
          onConfirm={() => this.handleDeleteConfirm(record.id)}
        >
          <a href="javascript: void(0);">删除</a>
        </Popconfirm>
      ),
    }];

    return columns;
  }

  render() {
    const menus = [{
      key: 'history',
      text: language.BROWSING_HISTORY,
      url: '/userInfo/history'
    }, {
      key: 'bookmark',
      text: language.BOOKMARK,
      url: '/userInfo/bookmark'
    }, {
      key: 'setting',
      text: language.SETTING,
      url: '/userInfo/setting'
    }];

    return (
      <Layout>
        <Container>
          <ShowCard ref="showCard">
            <SiderMenu
              selectedKeys={[this.state.current]}
              menus={menus}
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
      </Layout>
    );
  }
}
