'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Modal,
  Form,
  Input,
  Select
} from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class EditJobDescriptionForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      status: props.record.status
    };
    this.handleModalOK = this.handleModalOK.bind(this);
    this.handleStatusChange = this.handleStatusChange.bind(this);
  }
  
  componentWillReceiveProps(nextProps) {
    if (nextProps.visible) {
      this.setState({
        status: nextProps.record.status
      });
    }
  }

  handleModalOK() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onSubmit(Object.assign({}, values, { status: this.state.status }));
      }
    });
  }

  handleStatusChange(value) {
    this.setState({
      status: value
    });
  }

  render() {
    const {
      form,
      visible,
      confirmLoading,
      record,
      customerDataSource
    } = this.props,
    { getFieldDecorator } = form,
    { status } = this.state;
    
    const formItemLayout = {
      labelCol: { span: 6 },
      wrapperCol: { span: 16 },
    };

    const statusOptions = [{
      value: 'Opening',
      text: language.OPENING
    }, {
      value: 'Closed',
      text: language.CLOSED
    }];

    return (
      <Modal
        title={language.EDIT_JOB_DESCRIPTION}
        okText={language.SUBMIT}
        visible={visible}
        confirmLoading={confirmLoading}
        onOk={this.handleModalOK}
        onCancel={this.props.onCancel}
      >
        <Form layout="horizontal">
          <Form.Item
            {...formItemLayout}
            label={language.JOB_DESCRIPTION_ID}
          >
            {getFieldDecorator('id', {
              initialValue: record.id
            })(<Input readOnly />)}
          </Form.Item>
          <Form.Item
            {...formItemLayout}
            label={language.COMPANY_NAME}
          >
            {getFieldDecorator('company', {
              initialValue: record.company
            })(
              <Select disabled={true}>
                {customerDataSource.map(v => {
                  return (
                    <Select.Option key={v.id} value={v.id}>
                      {v.name}
                    </Select.Option>
                  );
                })}
              </Select>
            )}
          </Form.Item>
          <Form.Item
            {...formItemLayout}
            label={language.JOB_DESCRIPTION_CONTENT}
          >
            {getFieldDecorator('description', {
              initialValue: record.description,
              rules: [{ required: true }]
            })(
              <Input
                type="textarea"
                rows="6"
                disabled={record.committer !== localStorage.user}
              />
            )}
          </Form.Item>
          <Form.Item
            {...formItemLayout}
            label={language.COMMENTARY}
          >
            {getFieldDecorator('commentary', {
              initialValue: record.commentary
            })(<Input type="textarea" rows="2" />)}
          </Form.Item>
          <Form.Item
            {...formItemLayout}
            label={language.CURRENT_STATUS}
          >
            <Select value={status} onChange={this.handleStatusChange}>
              {statusOptions.map(v => <Select.Option key={v.value}>{v.text}</Select.Option>)}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    );
  }
}

EditJobDescriptionForm.propTypes = {
  form: PropTypes.object,
  visible: PropTypes.bool,
  confirmLoading: PropTypes.bool,
  record: PropTypes.object,
  customerDataSource: PropTypes.array,
  onSubmit: PropTypes.func,
  onCancel: PropTypes.func
};

export default EditJobDescriptionForm = Form.create({})(EditJobDescriptionForm);