'use strict';
import React, { Component, PropTypes } from 'react';

import { Input, Select } from 'antd';

import CreateJobDescription from './CreateJobDescription';

export default class ToolBar extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleSelectChange = this.handleSelectChange.bind(this);
  }

  handleChange(e) {
    this.props.onSearch(e.target.value);
  }

  handleSelectChange(value) {
    this.props.onSelectFilter(value);
  }

  render() {
    return (
      <div style={{ paddingTop: 10, paddingBottom: 10, }}>
        <CreateJobDescription {...this.props} />
        <div style={{ display: 'inline-block' }}>
          <label>Keyword: </label>
          <Input placeholder="Search" style={{ width: 160 }} onChange={this.handleChange} />
        </div>
        <div style={{ display: 'inline-block', marginLeft: 20 }}>
          <label>Status: </label>
          <Select
            style={{ width: 100 }}
            defaultValue={this.props.filter.status || ''}
            onChange={this.handleSelectChange}
          >
            <Select.Option key={0} value="">All</Select.Option>
            <Select.Option key={1} value="Opening">Open</Select.Option>
            <Select.Option key={2} value="Closed">Closed</Select.Option>
          </Select>
        </div>
        
      </div>
    );
  }
}

ToolBar.propTypes = {
  onSearch: PropTypes.func,
};