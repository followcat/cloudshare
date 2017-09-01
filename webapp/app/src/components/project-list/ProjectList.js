'use strict';
import React, { Component, PropTypes } from 'react';
import { checkAccount } from 'request/account'; 

import {
  Form,
  Input,
  Button,
  message,
} from 'antd';

const FormItem = Form.Item;

class ProjectList extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
    this.handleGetInput = this.handleGetInput.bind(this);
  }

  state = {
    result: false,
  };

  handleClick(e) {
    // e.preventDefault();

  this.props.form.validateFields((errors, values) => {
      if (!errors) {
        this.props.onSubmit(values);
      }
    });
  }


  handleGetInput() {
      this.props.form.validateFields((errors, values) => {
      if (!errors) {
        this.props.getInput(values);
      }
    });
  }

  render() {
    const { wrapperCol, btnText } = this.props,
          { getFieldDecorator } = this.props.form;

    return (
      <Form layout="horizontal" >
        <FormItem label={this.props.inputLabel}>
          {getFieldDecorator('name',{
            rules: [{
              required: true, message: '该栏是必填项',}
            ],
          })(
            <Input onBlur={this.handleGetInput}/>
          )}
        </FormItem>
      </Form>
    );
  }
}

ProjectList.defaultProps = {
  projects: [],
  wrapperCol: {},
  onSubmit() {},
  inputLabel: '',
};

ProjectList.propTypes = {
  projects: PropTypes.array,
  btnText: PropTypes.string,
  inputLabel: PropTypes.string,
  wrapperCol: PropTypes.object,
  form: PropTypes.object,
  onSubmit: PropTypes.func,
};

export default ProjectList = Form.create({})(ProjectList);
