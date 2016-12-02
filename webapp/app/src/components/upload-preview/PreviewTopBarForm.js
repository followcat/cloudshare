'use strict';
import React, { Component, PropTypes } from 'react';
import { Form, Input, Select, Button } from 'antd';
import { resumeSource } from '../../config/source';
const FormItem = Form.Item,
      Option = Select.Option;

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
    const props = this.props,
          { getFieldProps } = props.form;

    const nameProps = getFieldProps('name', {
      initialValue: props.name ? props.name : ''
    });

    const sourceProps = getFieldProps('origin');

    const classifyProps = getFieldProps('classify', {
      rules: [{ type: 'array' }]
    });

    return (
      <Form
        inline
        className={`${props.prefixCls}`}
      >
        <FormItem label="Name">
          <Input
            {...nameProps}
            placeholder="Please input name"
            style={{ width: 120 }}
          />
        </FormItem>
        <FormItem label="Source">
          <Select
            {...sourceProps}
            showSearch
            placeholder="Select a source"
            optionFilterProp="children"
            notFoundContent="Not found"
            style={{ width: 140 }}
          >
            {resumeSource.map(item => {
              return (
                <Option
                  key={item.id}
                  value={item.name}
                >
                  {item.name}
                </Option>
              );
            })}
          </Select>
        </FormItem>
        <FormItem label="Classify">
          <Select
            {...classifyProps}
            multiple
            placeholder="Select a classify"
            value={props.classifyValue}
            style={{ width: 160 }}
          >
            {props.classifyList.map((item, index) => {
              return (
                <Option
                  key={index}
                  value={item}
                  disabled
                >
                  {item}
                </Option>
              );
            })}
          </Select>
        </FormItem>
        {props.currentPreview === props.total - 1 ?
            <FormItem>
              <Button
                loading={props.confirmLoading}
                onClick={this.handleClick}
              >
                {props.btnText}
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
  name: PropTypes.string,
  classifyValue: PropTypes.array,
  classifyList: PropTypes.array,
  btnText: PropTypes.string,
  onConfirmClick: PropTypes.func,
};

export default PreviewTopBarForm;
