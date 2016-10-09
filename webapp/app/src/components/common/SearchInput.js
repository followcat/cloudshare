'use strict';
import React, { Component } from 'react';

import { Input, Button } from 'antd';

import classNames from 'classnames';

export default class SearchInput extends Component {

  constructor(props) {
    super(props);

    this.state = {
      value: '',
      focus: false,
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleFocusBlur = this.handleFocusBlur.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleInputChange(e) {
    this.setState({
      value: e.target.value,
    });
  }

  handleFocusBlur(e) {
    this.setState({
      focus: e.target === document.activeElement,
    });
  }

  handleSearch() {
    if (this.props.onSearch) {
      this.props.onSearch(this.state.value);
    }
  }

  componentDidMount() {
    this.setState({
      value: this.props.value,
    });
  }

  render() {
    const { style, size, placeholder } = this.props;

    const btnCls = classNames({
      'ant-search-btn': true,
      'ant-search-btn-noempty': !!this.state.value.trim(),
    });

    const searchCls = classNames({
      'ant-search-input': true,
      'ant-search-input-focus': this.state.focus,
    });

    return (
      <div className="ant-search-input-wrapper" style={style}>
        <Input.Group className={searchCls}>
          <Input
            placeholder={placeholder}
            value={this.state.value}
            onChange={this.handleInputChange}
            onFocus={this.handleFocusBlur}
            onBlur={this.handleFocusBlur}
            onPressEnter={this.handleSearch}
          />
          <div className="ant-input-group-wrap">
            <Button icon="search" className={btnCls} size={size} onClick={this.handleSearch} />
          </div>
        </Input.Group>
      </div>
    );
  }
}