'use strict';
import React, { Component, PropTypes } from 'react';
import { Form, Input, Button, Select } from 'antd';

const FormItem = Form.Item,
      SelectOption = Select.Option;

class SignInForm extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onSubmit(values);
      }
    });
  }

  render() {
    const { getFieldProps } = this.props.form,
          props = this.props;

    const accountProps = getFieldProps('account', {
      rules: [
        { required: true, message: 'Account is required.' },
      ],
    });

    const passwordProps = getFieldProps('password', {
      rules: [
        { required: true, message: 'Password is required.' },
        { min: 6, max: 18, message: 'Invalid Password. (At least 6-12 characters)' },
      ],
    });

    const projectProps = getFieldProps('project', {
      rules: [
        { required: true, message: 'Project is required.' }
      ],
    });

    return (
      <Form horizontal>
        <FormItem
          label="Account"
          id="account"
        >
          <Input {...accountProps} placeholder="Please input account." />
        </FormItem>
        <FormItem
          label="Password"
          id="password"
        >
          <Input {...passwordProps} type="password" placeholder="Please input password." />
        </FormItem>
        <FormItem
          label="Project"
          id="project"
        >
          <Select {...projectProps}>
            {this.props.projects.map((item, index) => {
              return (
                <SelectOption
                  key={index}
                  value={item}
                >
                  {item}
                </SelectOption>
              );
            })}
          </Select>
        </FormItem>
        <FormItem wrapperCol={props.wrapperCol}>
          <Button
            type="primary"
            onClick={this.handleClick}
          >
            {props.btnText}
          </Button>
        </FormItem>
      </Form>
    );
  }
}

SignInForm.defaultProps = {
  projects: [],
  btnText: 'Sign In',
  wrapperCol: {},
  onSUbmit() {},
};

SignInForm.propsTypes = {
  projects: PropTypes.array,
  btnText: PropTypes.string,
  wrapperCol: PropTypes.object,
  onSUbmit: PropTypes.func,
};

export default SignInForm = Form.create({})(SignInForm);
