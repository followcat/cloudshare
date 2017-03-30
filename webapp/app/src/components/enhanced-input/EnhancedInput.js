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
    this.handlekeyPress = this.handlekeyPress.bind(this);
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
    const props = this.props;

    if (props.onClick) {
      if (props.dataIndex) {
        let obj = {};
        obj[props.dataIndex] = this.state.value;
        props.onClick(obj);
      } else {
        props.onClick(this.state.value);
      }

      if (props.resettable) {
        this.setState({
          value: ''
        });
      }
    }
  }

  handlekeyPress(e) {
    if (e.key === 'Enter') {
      this.handleBtnClick();
    }
  }

  render() {
    const {
      prefixCls,
      style,
      placeholder,
      type,
      size
    } = this.props,
    { value, focus } = this.state;

    const btnCls = classNames({
      'ant-search-btn': true,
      'ant-search-btn-noempty': !!value.trim(),
    });
    const searchCls = classNames({
      'ant-search-input': true,
      'ant-search-input-focus': focus,
    });

    return (
      <div  className={prefixCls} style={style}>
        <InputGroup className={searchCls}>
          <Input
            placeholder={placeholder}
            value={this.state.value}
            onChange={this.handleInputChange}
            onFocus={this.handleFocusBlur}
            onBlur={this.handleFocusBlur}
            onKeyPress={this.handlekeyPress}
            onPressEnter={this.handleSearch}
            size={size || 'default'}
          />
          <div className="ant-input-group-wrap">
            <Button
              icon={type}
              className={btnCls}
              size={size || 'default'}
              onClick={this.handleBtnClick}
            />
          </div>
        </InputGroup>
      </div>
    );
  }
}

EnhancedInput.defaultProps = {
  prefixCls: 'ant-search-input-wrapper',
  type: 'search',
  placeholder: '',
  onClick() {},
  resettable: false,
};

EnhancedInput.propTypes = {
  prefixCls: PropTypes.string,
  type: PropTypes.oneOf(['search', 'plus']),
  size: PropTypes.string,
  style: PropTypes.object,
  placeholder: PropTypes.string,
  dataIndex: PropTypes.string,
  onClick: PropTypes.func,
  resettable: PropTypes.bool
};

export default EnhancedInput;
