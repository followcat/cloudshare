'use strict';
import React, { Component, PropTypes } from 'react';
import { Input, Button } from 'antd';
import classNames from 'classnames';

const InputGroup = Input.Group;

class EnhancedInput extends Component {
  constructor() {
    super();
    this.state = {
      value: '',
      focus: false,
    };
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleFocusBlur = this.handleFocusBlur.bind(this);
    this.handleBtnClick = this.handleBtnClick.bind(this);
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

  handleBtnClick() {
    if (this.props.onClick) {
      this.props.onClick(this.state.value);
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
              icon={props.type}
              className={btnCls}
              size={props.btnSize}
              onClick={this.handleBtnClick}
            />
          </div>
        </InputGroup>
      </div>
    );
  }
}

EnhancedInput.defaultProps = {
  type: 'search',
  placeholder: 'Please input text',
  onClick() {}
};

EnhancedInput.propTypes = {
  type: PropTypes.oneOf(['search', 'plus']),
  style: PropTypes.object,
  placeholder: PropTypes.string,
  btnSize: PropTypes.string,
  onClick: PropTypes.func,
};

export default EnhancedInput;
