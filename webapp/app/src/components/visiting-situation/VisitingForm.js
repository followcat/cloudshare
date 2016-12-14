'use strict';
import React, { Component, PropTypes } from 'react';
import { Form, Input, Button, DatePicker } from 'antd';
const FormItem = Form.Item;

class VisitingForm extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
    this.props.form.validateFields((errors, values) => {
      if (errors) {
        console.log(errors);
      }
      this.props.onSubmit(values);
    });
  }

  render() {
    const props = this.props,
          { getFieldProps } = props.form;

    return (
      <div className="cs-visiting-form">
        <div className="cs-visiting-form-icon">
          <span className="cs-visiting-form-user">{props.currentUser && props.currentUser.split('')[0].toUpperCase()}</span>
        </div>
        <Form
          inline
        >
          <FormItem>
            <Input
              {...getFieldProps('visitingText', {rules: [{ required: true }]})}
              placeholder={props.placeholder}
            />
          </FormItem>
          <FormItem>
            <DatePicker {...getFieldProps('visitingDate', {rules: [{ required: true }]})} />
          </FormItem>
          <FormItem>
            <Button
              type={props.btnType}
              onClick={this.handleClick}
            >
              {props.btnText}
            </Button>
          </FormItem>
        </Form>
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

export default VisitingForm = Form.create({})(VisitingForm);
