'use strict';
import React from 'react';
import { Link } from 'react-router';

import { Menu } from 'antd';

import Header from '../components/manage/Header';

import './manage.less';

export default class Manage extends React.Component {
  constructor() {
    super();
    this.state = {
      current: 'userList',
      wrapperHeigth: 0,
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    this.setState({
      current: e.key,
    });
  }

  componentDidMount() {
    let height = parseInt(this.refs.wrapper.offsetHeight) - 220;
    this.setState({
      wrapperHeigth: height,
    });
  }

  render() {
    return (
      <div>
        <div id="viewport">
          <Header fixed={true} />
          <div className="cs-layout-bottom">
            <div className="cs-layout-wrapper" ref="wrapper">
              <div className="cs-layout-sider">
                <Menu
                  mode="inline"
                  selectedKeys={[this.state.current]}
                  onClick={this.handleClick}
                >
                  <Menu.Item key="userList"><Link to="/userlist">User List</Link></Menu.Item>
                  <Menu.Item key="setting"><Link to="/setting">Setting</Link></Menu.Item>
                </Menu>
              </div>
              <div className="cs-layout-content">
                {this.props.children && React.cloneElement(this.props.children, { wrapperHeigth: this.state.wrapperHeigth })}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}