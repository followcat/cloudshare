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
    const props = this.props;

    return (
      <div className="cs-visiting-form">
        <div className="cs-visiting-form-icon">
          <span className="cs-visiting-form-user">
            {props.currentUser && props.currentUser.split('')[0].toUpperCase()}
          </span>
        </div>
        <div className="cs-visiting-form-field">
          <Input
            value={this.state.value}
            placeholder={props.placeholder}
            onChange={this.handleChange}
          />
          <Button
            type={props.btnType}
            onClick={this.handleClick}
          >
            {props.btnText}
          </Button>
        </div>
      </div>
    );
  }
}

VisitingForm.defaultProps = {
  placeholder: '',
  btnType: 'primary',
  btnText: 'Submit',
  onSubmit() {},
};

VisitingForm.propTypess = {
  placeholder: PropTypes.string,
  btnType: PropTypes.string,
  btnText: PropTypes.string,
  onSubmit: PropTypes.func,
};

export default VisitingForm;
