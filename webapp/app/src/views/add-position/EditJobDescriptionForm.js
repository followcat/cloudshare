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
      description: props.record.description,
      status: props.record.status,
      followup: props.record.followup,
      commentary: props.record.commentary
    };
    this.handleModalOK = this.handleModalOK.bind(this);
    this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
    this.handleStatusChange = this.handleStatusChange.bind(this);
    this.handleFollowupChange = this.handleFollowupChange.bind(this);
    this.handleCommentaryChange = this.handleCommentaryChange.bind(this);
  }
  
  componentWillReceiveProps(nextProps) {
    const { record } = nextProps;

    if (nextProps.visible) {
      this.setState({
        description: record.description,
        status: record.status,
        followup: record.followup,
        commentary: record.commentary
      });
    }
  }

  handleModalOK() {
    const {
      description,
      status,
      followup,
      commentary
    } = this.state;

    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onSubmit(Object.assign({}, values, {
          description: description,
          status: status,
          followup: followup,
          commentary: commentary
        }));
      }
    });
  }

  handleDescriptionChange(e) {
    this.setState({
      description: e.target.value
    });
  }

  handleStatusChange(value) {
    this.setState({
      status: value
    });
  }

  handleFollowupChange(e) {
    this.setState({
      followup: e.target.value
    });
  }

  handleCommentaryChange(e) {
    this.setState({
      commentary: e.target.value
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
    { description, status, followup, commentary } = this.state;
    
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
        style={{ top: 24 }}
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
            <Input
              type="textarea"
              rows="4"
              value={description}
              onChange={this.handleDescriptionChange}
              readOnly={record.committer !== localStorage.user}
            />
          </Form.Item>
          <Form.Item
            {...formItemLayout}
            label={language.REMARKS}
          >
            <Input
              type="textarea"
              rows="2"
              value={followup}
              onChange={this.handleFollowupChange}
            />
          </Form.Item>
          <Form.Item
            {...formItemLayout}
            label={language.COMMENTARY}
          >
            <Input
              type="textarea"
              rows="2"
              value={commentary}
              onChange={this.handleCommentaryChange}
            />
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