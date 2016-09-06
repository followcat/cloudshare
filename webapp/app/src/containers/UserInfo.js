'use strict';
import React, { Component } from 'react';
import { Link } from 'react-router';
import { Menu, message } from 'antd';
import 'whatwg-fetch';

import Header from '../components/common/Header';

import './manage.less';

export default class UserInfo extends Component {
  constructor() {
    super();
    this.state = {
      current: 'browsingHistory',
      historyHeight: 0,
      bookmarkHeight: 0,
      historyList: [],
      bookmarkList: [],
    };

    this.loadBrowsingHistory = this.loadBrowsingHistory.bind(this);
    this.loadBookmark = this.loadBookmark.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.onDeleteBookmark = this.onDeleteBookmark.bind(this);
  }

  loadBrowsingHistory() {
    let history = localStorage.history ? JSON.parse(localStorage.history) : [];
    this.setState({
      historyList: history,
    });
  }

  loadBookmark() {
    fetch(`/api/accounts/${localStorage.user}/bookmark`, {
      method: 'GET',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
      }
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          bookmarkList: json.data,  
        });
      } else {
        message.error(json.message);
        console.log(json);
      }
    });
  }

  onDeleteBookmark(id) {
    let _this = this;
    fetch(`/api/accounts/${localStorage.user}/bookmark`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        bookmark_id: id,
      })
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        message.success(json.message);
        _this.loadBookmark();
      } else {
        message.error(json.message);
      }
    })
  }

  handleClick(e) {
    this.setState({
      current: e.key,
    });
  }

  componentDidMount() {
    this.loadBrowsingHistory();
    this.loadBookmark();
    const height = parseInt(this.refs.wrapper.offsetHeight);
    let historyHeight = height - 120,
        bookmarkHeight = height - 180;
    this.setState({
      historyHeight: historyHeight,
      bookmarkHeight: bookmarkHeight,
    });
  }

  render() {
    return (
      <div>
        <div id="viewport">
          <Header />
          <div className="cs-layout-bottom">
            <div className="cs-layout-wrapper" ref="wrapper">
              <div className="cs-layout-sider">
                <Menu
                  mode="inline"
                  selectedKeys={[this.state.current]}
                  onClick={this.handleClick}
                >
                  <Menu.Item key="browsingHistory"><Link to="/browsingHistory">Browsing History</Link></Menu.Item>
                  <Menu.Item key="bookmark"><Link to="/bookmark">Bookmark</Link></Menu.Item>
                  <Menu.Item key="setting"><Link to="/setting">Setting</Link></Menu.Item>
                </Menu>
              </div>
              <div className="cs-layout-content">
                {this.props.children && React.cloneElement(
                  this.props.children, {
                    historyHeight: this.state.historyHeight,
                    bookmarkHeight: this.state.bookmarkHeight,
                    historyList: this.state.historyList,
                    bookmarkList: this.state.bookmarkList,
                    onDeleteBookmark: this.onDeleteBookmark,
                  })}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
