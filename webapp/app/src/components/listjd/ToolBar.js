'use strict';
import React, { Component, PropTypes } from 'react';

import { Input } from 'antd';

import CreateJobDescription from './CreateJobDescription';

export default class ToolBar extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    this.props.onSearch(e.target.value);
  }

  render() {
    return (
      <div style={{ paddingTop: 10, paddingBottom: 10, }}>
        <CreateJobDescription {...this.props} />
        <Input placeholder="Search" style={{ width: 200 }} onChange={this.handleChange}/>
      </div>
    );
  }
}

ToolBar.propTypes = {
  onSearch: PropTypes.func,
};