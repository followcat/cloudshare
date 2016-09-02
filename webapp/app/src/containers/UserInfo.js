'use strict';
import React, { Component } from 'react';
import { Link } from 'react-router';
import { Menu } from 'antd';

import Header from '../components/common/Header';

import './manage.less';

export default class UserInfo extends Component {
  constructor() {
    super();
    this.state = {
      current: 'browsingHistory',
      wrapperHeigth: 0,
      historyList: [],
    };

    this.loadBrowsingHistory = this.loadBrowsingHistory.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  loadBrowsingHistory() {
    let history = localStorage.history ? JSON.parse(localStorage.history) : [];
    this.setState({
      historyList: history,
    });
  }

  handleClick(e) {
    this.setState({
      current: e.key,
    });
  }

  componentDidMount() {
    this.loadBrowsingHistory();
    let height = parseInt(this.refs.wrapper.offsetHeight) - 120;
    this.setState({
      wrapperHeigth: height,
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
                </Menu>
              </div>
              <div className="cs-layout-content">
                {this.props.children && React.cloneElement(
                  this.props.children, {
                    wrapperHeigth: this.state.wrapperHeigth,
                    historyList: this.state.historyList,
                  })}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
