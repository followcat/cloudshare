'use strict';
import React, { Component, PropTypes } from 'react';

import ButtonWithModal from 'components/button-with-modal';

import { Form, Input, Select, Button } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class CreateNewJobDescription extends Component {
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
    const props = this.props,
          { getFieldDecorator } = props.form;

    return (
        <Form horizontal>
          <Form.Item label={language.COMPANY_NAME}>
            {getFieldDecorator('co_id', {
              rules: [{ required: true, message: language.COMPANY_NAME_VALIDATE_MSG }]
            })(
              <Select>
                {props.companyList.map(item => {
                  return (
                    <Select.Option
                      key={item.id}
                      value={item.id}
                    >
                      {item.name}
                    </Select.Option>
                  );
                })}
              </Select>
            )}
          </Form.Item>
          <Form.Item label={language.JOB_DESCRIPTION_NAME}>
            {getFieldDecorator('jd_name', {
              rules: [{ required: true, message: language.JOB_DESCRIPTION_NAME_VALIDATE_MSG, whitespace:true}]
            })(
              <Input />
            )}
          </Form.Item>
          <Form.Item label={language.JOB_DESCRIPTION_CONTENT}>
            {getFieldDecorator('jd_description', {
              rules: [{ required: true, message: language.JOB_DESCRIPTION_CONTENT_VALIDATE_MSG, whitespace:true }]
            })(
              <Input type="textarea" rows="4" />
            )}
          </Form.Item>
          <Form.Item>
            <Button type="primary" onClick={this.handleModalOk}>{language.CREATION}</Button>
          </Form.Item>
        </Form>
    );
  }
}

CreateNewJobDescription.defaultProps = {
  companyList: [],
  onCreate() {},
};

CreateNewJobDescription.propTypes = {
  form: PropTypes.object,
  companyList: PropTypes.array,
  onCreate: PropTypes.func,
};

export default CreateNewJobDescription = Form.create({})(CreateNewJobDescription);
