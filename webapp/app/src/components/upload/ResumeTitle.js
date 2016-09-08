'use strict';
import React, { Component } from 'react';

import { Form, Input, Select, Button, Icon } from 'antd';

class ResumeTitle extends Component {
  constructor(props){
    super(props);
    this.handlePrevClick = this.handlePrevClick.bind(this);
    this.handleNextClick = this.handleNextClick.bind(this);
  }

  handlePrevClick(e) {
    e.preventDefault();
    const fieldsValue = this.props.form.getFieldsValue();
    this.props.onPrevPreview(fieldsValue)
  }

  handleNextClick(e) {
    e.preventDefault();
    const fieldsValue = this.props.form.getFieldsValue();
    this.props.onNextPreview(fieldsValue);
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

    return (
      <div className="cs-preview-top">
        <Form inline style={{ width: 620, margin: '0 auto' }}>
          <Form.Item>
            <Button
              type="primary"
              size="small"
              disabled={this.props.index === 0 ? true : false}
              onClick={this.handlePrevClick}
            >
              <Icon type="left" />Prev
            </Button>
          </Form.Item>
          <Form.Item
            label="Name"
          >
            <Input
              {...getFieldProps('name', { initialValue: this.props.name ? this.props.name : '' })}
              type="text"
              placeholder="Please input resume name"
            />
          </Form.Item>
          <Form.Item
            label="Source"
          >
            <Select
              {...getFieldProps('source', { initialValue: sourceData[0].origin })}
              style={{ width: 200 }}
              defaultValue={sourceData[0].origin}
            >
              {sourceData.map((item) => {
                return (
                  <Select.Option key={item.num} value={item.origin}>{item.origin}</Select.Option>
                );
              })}
            </Select>
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              size="small"
              disabled={this.props.current === this.props.length - 1}
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