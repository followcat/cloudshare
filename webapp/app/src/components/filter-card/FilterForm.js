'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Row,
  Col,
  Form,
  Button,
  Input,
  Checkbox,
  Select,
  DatePicker,
  Icon
} from 'antd';

import moment from 'moment';

const FormItem = Form.Item,
      CheckboxGroup = Checkbox.Group,
      RangePicker = DatePicker.RangePicker,
      Option = Select.Option,
      OptGroup = Select.OptGroup;

class FilterForm extends Component {
  constructor() {
    super();
    this.state = {
      expand: false,
      gender: [],
      education: [],
      maritalStatus: []
    };
    this.handleGenderChange = this.handleGenderChange.bind(this);
    this.handleEducationChange = this.handleEducationChange.bind(this);
    this.handleMaritalStatusChange = this.handleMaritalStatusChange.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleReset = this.handleReset.bind(this);
    this.handleToggle = this.handleToggle.bind(this);
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

      const dateValue = values['date'];

      const formValues = Object.assign({}, {
        ...values,
        'date': dateValue ? [dateValue[0].format('YYYY-MM-DD'), dateValue[1].format('YYYY-MM-DD')] : ['', '']
      }, {
        gender: this.state.gender,
        education: this.state.education,
        marital_status: this.state.maritalStatus
      });

      this.props.onSearch(formValues);
    });
  }

  handleReset(e) {
    e.preventDefault();
    this.props.form.resetFields();

    this.setState({
      gender: [],
      education: [],
      maritalStatus: []
    });
  }

  handleToggle(e) {
    e.preventDefault();
    this.setState({
      expand: !this.state.expand
    });
  }

  disabledDate(current) {
    return current && current.valueOf() > Date.now();
  }

  renderIndustry() {
    const { industry } = this.props;
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
    const { textarea, databaseDisplay, classify  } = this.props;
    const { getFieldDecorator } = this.props.form;
    const { expand } = this.state;

    const genderOptions = [
      { label: '男', value: '男' },
      { label: '女', value: '女' },
    ];

    const educationOptions = [
      { label: '大专', value: '大专' },
      { label: '本科', value: '本科' },
      { label: '硕士', value: '硕士' },
      { label: '博士', value: '博士' }
    ];

    const maritalStatusOptions = [
      { label: '未婚', value: '未婚' },
      { label: '已婚', value: '已婚' }
    ];

    const formItemLayout = {
      labelCol: { span: 5 },
      wrapperCol: { span: 19 }
    };

    return (
      <Form layout="horizontal">
        {textarea ?
          <Row>
            <Col>
              <FormItem
                label="职位描述"
                labelCol={{ span: 3 }}
                 wrapperCol={{ span: 19 }}
              >
                {getFieldDecorator('doc')(
                  <Input type="textarea" rows={1} />)}
              </FormItem>
            </Col>
          </Row> : null}
        {databaseDisplay ? 
          <Row>
            <Col span={24}>
              <Form.Item
                label="选择数据库"
                className="classify-selection"
                labelCol={{ span: 3 }}
                wrapperCol={{ span: 19 }}
              >
                {getFieldDecorator('uses', {
                  initialValue: textarea ? [] : classify,
                  rules: [{ type: 'array' }]
                })(<Select multiple>
                    {classify.map((item, index) => {
                      return <Option key={index} value={item} >{item}</Option>
                    })}
                  </Select>)}
              </Form.Item>
            </Col>
          </Row> : null}
        <Row gutter={8}>
          <Col span={8}>
            <FormItem
              label="性别"
              {...formItemLayout}
            >
              <CheckboxGroup
                options={genderOptions}
                onChange={this.handleGenderChange}
              />
            </FormItem>
          </Col>
          <Col span={8}>
            <FormItem
              label="学历"
              {...formItemLayout}
            >
              <CheckboxGroup
                options={educationOptions}
                onChange={this.handleEducationChange}
              />
            </FormItem>
          </Col>
          <Col span={8}>
            <FormItem
              label="婚姻状况"
              {...formItemLayout}
            >
              <CheckboxGroup
                options={maritalStatusOptions}
                onChange={this.handleMaritalStatusChange}
              />
            </FormItem>
          </Col>
          {expand ?
            <div>
              <Col span={8}>
                <FormItem
                  label="时间"
                  {...formItemLayout}
                >
                  {getFieldDecorator('date')(
                    <RangePicker
                      disabledDate={this.disabledDate}
                    />)}
                </FormItem>
              </Col>
              <Col span={8}>
                <FormItem
                  label="当前地点"
                  {...formItemLayout}
                >
                  {getFieldDecorator('current_places')(
                    <Input />)}
                </FormItem>
              </Col>
              <Col span={8}>
                <FormItem
                  label="期望地点"
                  {...formItemLayout}
                >
                  {getFieldDecorator('expectation_places')(
                    <Input />)}
                </FormItem>
              </Col>
              <Col span={8}>
                <FormItem
                  label="行业"
                  {...formItemLayout}
                >
                  {getFieldDecorator('business')(
                    <Select
                      showSearch={true}
                      multiple={true}
                    >
                      {this.renderIndustry()}
                    </Select>)}
                </FormItem>
              </Col>
            </div> :
          null}
        </Row>
        <Row>
          <Col span={5} offset={10}>
            <Button type="primary" onClick={this.handleSearch}>搜索</Button>
            <Button style={{ marginLeft: 8 }} onClick={this.handleReset}>重置</Button>
            <a style={{ marginLeft: 8, fontSize: 12 }} onClick={this.handleToggle}>
              折叠 <Icon type={expand ? 'up' : 'down'} />
            </a>
          </Col>
        </Row>
      </Form>
    );
  }
}

FilterForm.defaultProps = {
  databaseDisplay: true
};

FilterForm.propTypes = {
  textarea: PropTypes.bool,
  industry: PropTypes.objectOf(PropTypes.array),
  classify: PropTypes.array,
  form: PropTypes.object,
  onSearch: PropTypes.func
};

export default FilterForm = Form.create({})(FilterForm);
