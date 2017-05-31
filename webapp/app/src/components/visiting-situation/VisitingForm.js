'use strict';
import React, { Component, PropTypes } from 'react';
import { Input, Button } from 'antd';

class VisitingForm extends Component {
  constructor() {
    super();
    this.state = {
      value: '',
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
    const fieldValue = this.state.value;
    if (fieldValue) {
      this.props.onSubmit(fieldValue);
      this.setState({
        value: '',
      });
    }
  }

  handleChange(e) {
    this.setState({
      value: e.target.value,
    });
  }

  render() {
    const {
      prefixCls,
      currentUser,
      placeholder,
      btnType,
      btnText
    } = this.props,
    { value } = this.state;

    return (
      <div className={prefixCls}>
        <div className={`${prefixCls}-icon`}>
          <span className={`${prefixCls}-user`}>
            {currentUser && currentUser.split('')[0].toUpperCase()}
          </span>
        </div>
        <div className={`${prefixCls}-field`}>
          <Input
            value={value}
            placeholder={placeholder}
            onChange={this.handleChange}
          />
          <Button
            type={btnType}
            onClick={this.handleClick}
          >
            {btnText}
          </Button>
        </div>
      </div>
    );
  }
}

VisitingForm.defaultProps = {
  prefixCls: 'cs-visiting-form',
  placeholder: '',
  btnType: 'primary',
  btnText: 'Submit',
  onSubmit() {}
};

VisitingForm.propTypes = {
  prefixCls: PropTypes.string,
  placeholder: PropTypes.string,
  currentUser: PropTypes.array,
  btnType: PropTypes.string,
  btnText: PropTypes.string,
  onSubmit: PropTypes.func
};

export default VisitingForm;
