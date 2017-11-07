'use strict';
import React, { Component, PropTypes } from 'react';

import { Form, Input, Select, Button } from 'antd';

import { getUploadOrigin } from 'request/classify';

const FormItem = Form.Item,
      Option = Select.Option;

class PreviewTopBarForm extends Component {
  constructor() {
    super();
    this.state = {
      origins: []
    }
    this.handleClick = this.handleClick.bind(this);
  }

  componentWillMount() {
    getUploadOrigin((json) => {
      if (json.code === 200) {
        this.setState({
          origins: json.data,
        });
      }
    });
  }

  handleClick(e) {
    e.preventDefault();

    const fieldsValue = this.props.form.getFieldsValue();

    this.props.onConfirmClick({
      id: this.props.id,
      fieldsValue: fieldsValue
    });
  }

  render() {
    const {
      form,
      name,
      prefixCls,
      resumeID,
      classifyValue,
      classifyList,
      currentPreview,
      total,
      confirmLoading,
      btnText
    } = this.props,
    { getFieldDecorator } = form;
    const { origins } = this.state;

    return (
      <Form layout="inline" className={`${prefixCls}-form`}>
        <FormItem label="简历ID">
          {getFieldDecorator('resumeID', {
            initialValue: resumeID || ''
          })(
            <Input
              style={{ width: 120 }}
              readOnly
              size="small"
            />
          )}
          
        </FormItem>
        <FormItem label="候选人名字">
          {getFieldDecorator('name', {
            initialValue: name || ''
          })(
            <Input
              placeholder="请输入候选人名字"
              style={{ width: 100 }}
              size="small"
            />
          )}
        </FormItem>
        <FormItem label="简历来源">
          {getFieldDecorator('origin')(
            <Select
              showSearch
              placeholder="选择简历来源"
              optionFilterProp="children"
              notFoundContent="Not found"
              style={{ width: 120 }}
              size="small"
            >
              {origins.map(item => {
                return (
                  <Option key={item.id} value={item.name}>{item.name}</Option>
                );
              })}
            </Select>
          )}
        </FormItem>
        <FormItem label="行业">
          {getFieldDecorator('classify', {
            initialValue: classifyValue,
            rules: [{ type: 'array' }]
          })(
            <Select
              multiple
              style={{ width: 120 }}
              size="small"
            >
              {classifyList.map((item, index) => {
                return (
                  <Option key={index} value={item} disabled>{item}</Option>
                );
              })}
            </Select>
          )}
        </FormItem>
        {currentPreview === total - 1 ?
          <FormItem>
            <Button
              type="primary"
              loading={confirmLoading}
              onClick={this.handleClick}
              size="small"
            >
              {btnText}
            </Button>
          </FormItem> :
          null
        }
      </Form>
    );
  }
}

PreviewTopBarForm.defaultProps = {
  prefixCls: 'cs-preview-top-bar-form',
  name: '',
  classifyValue: [],
  classifyList: [],
  btnText: 'Confirm',
  onConfirmClick() {},
};

PreviewTopBarForm.propTypes = {
  prefixCls: PropTypes.string,
  id: PropTypes.string,
  name: PropTypes.string,
  classifyValue: PropTypes.array,
  classifyList: PropTypes.array,
  btnText: PropTypes.string,
  resumeID: PropTypes.string,
  currentPreview: PropTypes.number,
  total: PropTypes.number,
  confirmLoading: PropTypes.bool,
  form: PropTypes.object,
  onConfirmClick: PropTypes.func,
};

export default PreviewTopBarForm;
