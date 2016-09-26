'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col, Form, Select, Input, Checkbox, Button } from 'antd';

class FilterForm extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const genderChildren = [
      {
        text: 'Male',
        value: '男',
      }, {
        text: 'Female',
        value: '女',
      },
    ];

    const educationChildren = [
      {
        text: 'College',
        value: '大专',
      }, {
        text: 'Undergraduate',
        value: '本科',
      }, {
        text: 'Master',
        value: '硕士',
      }, {
        text: 'PhD',
        value: '博士',
      },
    ];

    const maritalStatusChildren = [
      {
        text: 'Unmarried',
        value: '未婚',
      }, {
        text: 'Married',
        value: '已婚',
      },
    ];

    return (
      <Form horizontal>
        <Row>
          <Col>
            <Form.Item
              label="Classify"
              labelCol={{ span: 3 }}
              wrapperCol={{ span: 8 }}
            >
              <Select
                multiple
              >
                {this.props.classify.map((item, index) => {
                  return <Select.Option key={index} value={item} >{item}</Select.Option>
                })}
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={8}>
          <Col span={12}>
            <Form.Item
              label="Gender"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              {genderChildren.map((item, index) => {
                return <Checkbox key={index} className="ant-checkbox-inline" value={item.value}>{item.text}</Checkbox>
              })}
            </Form.Item>
            <Form.Item
              label="Education"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              {educationChildren.map((item, index) => {
                return <Checkbox key={index} className="ant-checkbox-inline" value={item.value}>{item.text}</Checkbox>
              })}
            </Form.Item>
            <Form.Item
              label="Marital Status"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              {maritalStatusChildren.map((item, index) => {
                return <Checkbox key={index} className="ant-checkbox-inline" value={item.value}>{item.text}</Checkbox>
              })}
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Current Places"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 16 }}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="Expectation Places"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 16 }}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="Industry"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 16 }}
            >
              <Input />
            </Form.Item>
          </Col>
        </Row>
        <Row>
          <Col span={4} offset={10}>
            <Button type="primary" >Search</Button>
            <Button style={{ marginLeft: 8 }}>Reset</Button>
          </Col>
        </Row>
      </Form>
    );
  }
}

FilterForm.propTypes = {
  classify: PropTypes.array,
};

export default FilterForm = Form.create({})(FilterForm);
