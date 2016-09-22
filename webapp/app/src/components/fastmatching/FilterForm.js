'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col, Form, Select, Input, Checkbox, Button } from 'antd';

class FilterForm extends Component {

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
                <Select.Option key={0} value="计算机软件" >计算机软件</Select.Option>
                <Select.Option key={1} value="计算机硬件">计算机硬件</Select.Option>
                <Select.Option key={2} value="生物-制药-医疗器械">生物-制药-医疗器械</Select.Option>
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
          <Col span={8} offset={10}>
            <Button type="primary" >Search</Button>
            <Button style={{ marginLeft: 8 }}>Reset</Button>
          </Col>
        </Row>
      </Form>
    );
  }
}

export default FilterForm = Form.create({})(FilterForm);
