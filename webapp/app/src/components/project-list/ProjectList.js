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
    this.handleKeyPress = this.handleKeyPress.bind(this);
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

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.handleClick();
    }
  }

  handleGetInput() {
      this.props.form.validateFields((errors, values) => {
      if (!errors) {
        this.props.getProjectName(values);
      }
    });
  }

  render() {
    const { wrapperCol, btnText } = this.props,
          { getFieldDecorator } = this.props.form;

    return (
      <Form layout="horizontal" onSubmit={this.handleClick} onKeyPress={this.handleKeyPress}>
        <FormItem label="项目名称">
          {getFieldDecorator('projectname',{
            rules: [{
              required: true, message: '项目名称是必填项',}
            ],
          })(
            <Input onChange={this.handleGetInput}/>
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
};

ProjectList.propTypes = {
  projects: PropTypes.array,
  btnText: PropTypes.string,
  wrapperCol: PropTypes.object,
  form: PropTypes.object,
  onSubmit: PropTypes.func,
};

export default ProjectList = Form.create({})(ProjectList);
