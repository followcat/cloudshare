'use strict';
import React, { Component } from 'react';

import { Form, Input, Select, Button, Icon } from 'antd';

import ResumeComfirm from './ResumeComfirm';
import IndustrySingleSelection from '../common/IndustrySingleSelection';

class ResumeTitle extends Component {
  constructor(props){
    super(props);
    this.handlePrevClick = this.handlePrevClick.bind(this);
    this.handleNextClick = this.handleNextClick.bind(this);
  }

  handlePrevClick(e) {
    e.preventDefault();
    const fieldsValue = this.props.form.getFieldsValue();
    let value = Object.assign(fieldsValue, { id: this.props.yaml_info.id });
    this.props.onPrevPreview(value);
  }

  handleNextClick(e) {
    e.preventDefault();
    const fieldsValue = this.props.form.getFieldsValue();
    let value = Object.assign(fieldsValue, { id: this.props.yaml_info.id });
    this.props.onNextPreview(value);
  }

  render() {
    const { getFieldProps } = this.props.form;

    const sourceData = [
      { "num" : 1, "origin" : "前程无忧" },
      { "num" : 2, "origin" : "无忧精英" },
      { "num" : 3, "origin" : "智联招聘" },
      { "num" : 4, "origin" : "智联卓聘" },
      { "num" : 5, "origin" : "猎聘" },
      { "num" : 6, "origin" : "领英" },
      { "num" : 7, "origin" : "大街网" },
      { "num" : 8, "origin" : "Cold Call" },
      { "num" : 9, "origin" : "其他" }
    ];

    const isLastPreview = this.props.current === this.props.length - 1;

    return (
      <div className="cs-preview-top">
        <Form inline style={{ position: 'relative' }}>
          <Form.Item
            style={{ position: 'absolute', top: 0, left: 0 }}
          >
            <Button
              type="primary"
              size="small"
              disabled={this.props.index === 0 || this.props.disabled}
              onClick={this.handlePrevClick}
            >
              <Icon type="left" />Prev
            </Button>
          </Form.Item>
          <div style={{ width: 720, margin: '0 auto' }}>
            <Form.Item
              label="Name"
            >
              <Input
                {...getFieldProps('name', { initialValue: this.props.name ? this.props.name : '' })}
                style={{ width: 120 }}
                type="text"
                placeholder="Input resume name"
              />
            </Form.Item>
            <Form.Item
              label="Source"
            >
              <Select
                {...getFieldProps('source')}
                showSearch
                style={{ width: 140 }}
                placeholder="Select a source"
                optionFilterProp="children"
                notFoundContent="Not found"
              >
                {sourceData.map((item) => {
                  return (
                    <Select.Option key={item.num} value={item.origin}>{item.origin}</Select.Option>
                  );
                })}
              </Select>
            </Form.Item>
            <Form.Item
              label="Industry"
            >
              <Select
                {...getFieldProps('industry')}
                showSearch
                style={{ width: 160 }}
                placeholder="Select a industry"
                optionFilterProp="children"
                notFoundContent="Not found"
              >
                {this.props.industryList.map((item, index) => {
                  return (
                    <Select.Option key={index} value={item}>{item}</Select.Option>
                  );
                })}
              </Select>
            </Form.Item>
            <Form.Item>
              {isLastPreview ? <ResumeComfirm {...this.props} /> : ''}
            </Form.Item>
          </div>
          <Form.Item
            style={{ position: 'absolute', top: 0, right: 0 }}
          >
            <Button
              type="primary"
              size="small"
              disabled={isLastPreview}
              onClick={this.handleNextClick}
            >
              Next<Icon type="right" />
            </Button>
          </Form.Item>
        </Form>
      </div>
    );
  }
}

export default ResumeTitle = Form.create({})(ResumeTitle);