'use strict';
import React, { Component, PropTypes } from 'react';
import { Input, Button } from 'antd';
import classNames from 'classnames';

const InputGroup = Input.Group;

class SearchInput extends Component {
  constructor() {
    super();
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

  render() {
    const props = this.props;

    const btnCls = classNames({
      'ant-search-btn': true,
      'ant-search-btn-noempty': !!this.state.value.trim(),
    });
    const searchCls = classNames({
      'ant-search-input': true,
      'ant-search-input-focus': this.state.focus,
    });

    return (
      <div 
        className="ant-search-input-wrapper"
        style={props.style}
      >
        <InputGroup className={searchCls}>
          <Input
            placeholder={props.placeholder}
            value={this.state.value}
            onChange={this.handleInputChange}
            onFocus={this.handleFocusBlur}
            onBlur={this.handleFocusBlur}
            onPressEnter={this.handleSearch}
          />
          <div className="ant-input-group-wrap">
            <Button
              icon="search"
              className={btnCls}
              size={props.btnSize}
              onClick={this.handleSearch}
            />
          </div>
        </InputGroup>
      </div>
    );
  }
}

SearchInput.defaultProps = {
  placeholder: 'Please input search text',
  onSearch() {}
};

SearchInput.propTypes = {
  style: PropTypes.object,
  placeholder: PropTypes.string,
  btnSize: PropTypes.string,
  onSearch: PropTypes.func,
};

export default SearchInput;
