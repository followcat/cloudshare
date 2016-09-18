'use strict';
import React, { Component } from 'react';
import { Link } from 'react-router';
import { Menu, message } from 'antd';
import 'whatwg-fetch';


import Header from '../components/common/Header';

import './manage.less';

export default class ListJD extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      current: 'jobdescription',
      jobDescriptionData: [],
      companyData: [],
      height: 0,
    };
    this.loadJobDescription = this.loadJobDescription.bind(this);
  }

  loadJobDescription() {
    fetch(`/api/jdlist`, {
      method: 'GET',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
      },
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        let data = [];
        data = json.data.map((item, index) => {
          if (!item.key) {
            return Object.assign(item, { key: index });
          }
          return item;
        });
        this.setState({
          jobDescriptionData: data,
        });
      }
    })
  }

  componentDidMount() {
    this.loadJobDescription();
    const height = parseInt(this.refs.wrapper.offsetHeight) - 160;
    this.setState({
      height: height,
    });
  }

  handleMenuClick(e) {
    this.setState({
      current: e.key,
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
                  onClick={this.handleMenuClick}
                >
                  <Menu.Item key="jobdescription"><Link to="/jobdescription">Job Description</Link></Menu.Item>
                  <Menu.Item key="company"><Link to="/company">Company</Link></Menu.Item>
                </Menu>
              </div>
              <div className="cs-layout-content">
                {this.props.children && React.cloneElement(
                  this.props.children, {
                    jobDescriptionData: this.state.jobDescriptionData,
                    height: this.state.height,
                  })}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}