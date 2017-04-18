'use strict';
import React, { Component, PropTypes } from 'react';

import { Select, Input, Icon } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

const options = [{
  key: 'name',
  text: language.COMPANY_NAME
}, {
  key: 'responsible',
  text: language.RESPONSIBLE
}, {
  key: 'priority',
  text: language.PRIORITY
}, {
  key: 'clientcontact',
  text: language.CONTACT
}, {
  key: 'progress',
  text: language.VISITING_SITUATION
}, {
  key: 'district',
  text: language.DISTRICT
}];

class FilterCondition extends Component {
  constructor() {
    super();
    this.state = {
      filterKey: options[0].key,
      filterValue: ''
    };
    this.handleFilterSelect = this.handleFilterSelect.bind(this);
    this.handleFilterChange = this.handleFilterChange.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  componentDidMount() {
    const { index } = this.props,
          { filterKey } = this.state;

    this.props.updateFilterCondition(index, 'key', filterKey);
  }

  handleFilterSelect(value) {
    const { index } = this.props;

    this.setState({
      filterKey: value
    });

    this.props.updateFilterCondition(index, 'key', value);
  }

  handleFilterChange(e) {
    const { index } = this.props;

    this.setState({
      filterValue: e.target.value
    });

    this.props.updateFilterCondition(index, 'value', e.target.value);
  }

  handleClose() {
    const{ index } = this.props;

    this.props.updateFilterCondition(index, 'delete');
  }

  render() {
    const { filterKey, filterValue } = this.state;

    return (
      <div className="filter-condition">
        <Select value={filterKey} onSelect={this.handleFilterSelect}>
          {options.map(item => <Select.Option key={item.key}>{item.text}</Select.Option>)}
        </Select>
        <Input
          placeholder="请输入关键字"
          value={filterValue}
          onChange={this.handleFilterChange}
        />
        <span className="close-icon">
          <Icon type="close-square-o" onClick={this.handleClose} />
        </span>
      </div>
    );
  }
}

FilterCondition.propTypes = {
  index: PropTypes.number,
  updateFilterCondition: PropTypes.func
};

export default FilterCondition;
