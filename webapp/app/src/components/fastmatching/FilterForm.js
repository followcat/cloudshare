'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col, Form, Select, Input, Checkbox, Button } from 'antd';

class FilterForm extends Component {

  constructor(props) {
    super(props);
    
    this.state = {
      gender: [],
      education: [],
      maritalStatus: [],
    };

    this.handleGenderChange = this.handleGenderChange.bind(this);
    this.handleEducationChange = this.handleEducationChange.bind(this);
    this.handleMaritalStatusChange = this.handleMaritalStatusChange.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleReset = this.handleReset.bind(this);
  }

  handleGenderChange(values) {
    this.setState({
      gender: values,
    });
  }

  handleEducationChange(values) {
    this.setState({
      education: values,
    });
  }

  handleMaritalStatusChange(values) {
    this.setState({
      maritalStatus: values,
    });
  }

  handleSearch() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      }
      let formValues = Object.assign(values, {
        gender: this.state.gender,
        education: this.state.education,
        marital_status: this.state.maritalStatus,
      });
      this.props.onSearch(formValues);
    });
  }

  handleReset(e) {
    e.preventDefault();
    this.props.form.resetFields();
  }

  render() {

    const genderOptions = [
      { label: 'Male', value: '男' },
      { label: 'Female', value: '女' },
    ];

    const educationOptions = [
      { label: 'College', value: '大专' },
      { label: 'Undergraduate', value: '本科' },
      { label: 'Master', value: '硕士' },
      { label: 'PhD', value: '博士' },
    ];

    const maritalStatusOptions = [
      { label: 'Unmarried', value: '未婚' },
      { label: 'Married', value: '已婚' },
    ];

    const { getFieldProps } = this.props.form;

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
                {...getFieldProps('uses', {
                  rules: [
                    { required: true, type: 'array', message: 'Classify is required.' },
                  ],
                })}
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
              <Checkbox.Group options={genderOptions} onChange={this.handleGenderChange} />
            </Form.Item>
            <Form.Item
              label="Education"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              <Checkbox.Group options={educationOptions} onChange={this.handleEducationChange} />
            </Form.Item>
            <Form.Item
              label="Marital Status"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              <Checkbox.Group options={maritalStatusOptions} onChange={this.handleMaritalStatusChange} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Current Places"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 16 }}
            >
              <Input
                {...getFieldProps('current_places')}
              />
            </Form.Item>
            <Form.Item
              label="Expectation Places"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 16 }}
            >
              <Input
                {...getFieldProps('expectation_places')}
              />
            </Form.Item>
            <Form.Item
              label="Industry"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 16 }}
            >
              <Input
                {...getFieldProps('business')}
              />
            </Form.Item>
          </Col>
        </Row>
        <Row>
          <Col span={4} offset={10}>
            <Button type="primary" onClick={this.handleSearch}>Search</Button>
            <Button style={{ marginLeft: 8 }} onClick={this.handleReset}>Reset</Button>
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
