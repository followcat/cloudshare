'use strict';
import React, { Component, PropTypes } from 'react';

import { Form, Input, Select, Button } from 'antd';

import { resumeSource } from 'config/source';

const FormItem = Form.Item,
      SelectOption = Select.Option;

class PreviewTopBarForm extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
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
      { getFieldProps } = form;

    const nameProps = getFieldProps('name', {
      initialValue: name || ''
    });

    const sourceProps = getFieldProps('origin');

    const classifyProps = getFieldProps('classify', {
      rules: [{ type: 'array' }]
    });

    return (
      <Form inline className={`${prefixCls}-form`}>
        <FormItem label="ID">
          <Input
            style={{ width: 120 }}
            value={resumeID}
            readOnly
          />
        </FormItem>
        <FormItem label="Name">
          <Input
            {...nameProps}
            placeholder="Please input name"
            style={{ width: 100 }}
          />
        </FormItem>
        <FormItem label="Source">
          <Select
            {...sourceProps}
            showSearch
            placeholder="Select a source"
            optionFilterProp="children"
            notFoundContent="Not found"
            style={{ width: 120 }}
          >
            {resumeSource.map(item => {
              return (
                <SelectOption key={item.id} value={item.name}>{item.name}</SelectOption>
              );
            })}
          </Select>
        </FormItem>
        <FormItem label="Classify">
          <Select
            {...classifyProps}
            multiple
            placeholder="Select a classify"
            value={classifyValue}
            style={{ width: 120 }}
          >
            {classifyList.map((item, index) => {
              return (
                <SelectOption key={index} value={item} disabled>{item}</SelectOption>
              );
            })}
          </Select>
        </FormItem>
        {currentPreview === total - 1 ?
          <FormItem>
            <Button loading={confirmLoading} onClick={this.handleClick}>{btnText}</Button>
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
