'use strict';
import React, { Component, PropTypes } from 'react';
import ButtonWithModal from '../button-with-modal';
import { Form, Input } from 'antd';
const FormItem = Form.Item;

class CreateNewCompany extends Component {
  constructor() {
    super();
    this.handleModalOk = this.handleModalOk.bind(this);
  }

  handleModalOk() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onCreate(values);
        this.props.form.resetFields();
      }
    });
  }

  render() {
    const { getFieldProps } = this.props.form;

    return (
      <ButtonWithModal
        {...this.props}
        onModalOk={this.handleModalOk}
      >
        <Form>
          <FormItem
            label="Company Name"
          >
            <Input
              {...getFieldProps('companyName', { rules: [{ required: true }] })}
              placeholder="Please input company name."
            />
          </FormItem>
          <FormItem
            label="Introduction"
          >
            <Input
              {...getFieldProps('introduction')}
              type="textarea"
              rows="4"
            />
          </FormItem>
        </Form>
      </ButtonWithModal>
    );
  }
}

CreateNewCompany.defaultProps = {
  onCreate() {},
};

CreateNewCompany.propTypes = {
  onCreate: PropTypes.func,
};

export default CreateNewCompany = Form.create({})(CreateNewCompany);
