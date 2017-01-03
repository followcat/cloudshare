'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col, Form, Select, Input, Checkbox, Button, DatePicker } from 'antd';

const RangePicker = DatePicker.RangePicker,
      Option = Select.Option,
      OptGroup = Select.OptGroup;

class FilterForm extends Component {

  constructor(props) {
    super(props);
    
    this.state = {
      gender: [],
      education: [],
      maritalStatus: [],
      date: [],
    };

    this.handleGenderChange = this.handleGenderChange.bind(this);
    this.handleEducationChange = this.handleEducationChange.bind(this);
    this.handleMaritalStatusChange = this.handleMaritalStatusChange.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleReset = this.handleReset.bind(this);
    this.handleRangePickerChange = this.handleRangePickerChange.bind(this);
    this.disabledDate = this.disabledDate.bind(this);
    this.renderIndustry = this.renderIndustry.bind(this);
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
        date: this.state.date,
      });
      this.props.onSearch(formValues);
    });
  }

  handleReset(e) {
    e.preventDefault();
    this.props.form.resetFields();
  }

  handleRangePickerChange(value, dateString) {
    this.setState({
      date: dateString
    });
  }

  disabledDate(current) {
    return current && current.getTime() > Date.now();
  }

  renderIndustry() {
    const industry = this.props.industry;
    let optGroup = [];

    for (let key in industry) {
      optGroup.push(
        <OptGroup key={key} label={key}>
          {industry[key].map(item => <Option key={item} value={item}>{item}</Option>)}
        </OptGroup>
      );
    }

    return optGroup;
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
        {this.props.textarea ? 
          <Row>
            <Col>
              <Form.Item
                label="Job description"
                labelCol={{ span: 3 }}
                wrapperCol={{ span: 8 }}
              >
                <Input
                  {...getFieldProps('doc')}
                  type="textarea"
                  rows={1}
                />
              </Form.Item>
            </Col>
          </Row> : ''}
        <Row gutter={8}>
          <Col span={12}>
            <Form.Item
              label="Classify"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              <Select
                {...getFieldProps('uses', {
                  rules: [
                    { type: 'array' },
                  ],
                })}
                multiple
              >
                {this.props.classify.map((item, index) => {
                  return <Option key={index} value={item} >{item}</Option>
                })}
              </Select>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Date"
              labelCol={{ span: 8}}
              wrapperCol={{ span: 16 }}
            >
              <RangePicker
                {...getFieldProps('date')}
                value={this.state.date}
                disabledDate={this.disabledDate}
                onChange={this.handleRangePickerChange}
              />
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
              <Checkbox.Group
                options={genderOptions}
                onChange={this.handleGenderChange}
              />
            </Form.Item>
            <Form.Item
              label="Education"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              <Checkbox.Group
                options={educationOptions}
                onChange={this.handleEducationChange}
              />
            </Form.Item>
            <Form.Item
              label="Marital Status"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 18 }}
            >
              <Checkbox.Group
                options={maritalStatusOptions}
                onChange={this.handleMaritalStatusChange}
              />
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
              <Select
                {...getFieldProps('business')}
                showSearch={true}
              >
                {this.renderIndustry()}
              </Select>
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
  onSearch: PropTypes.func,
};

export default FilterForm = Form.create({})(FilterForm);
