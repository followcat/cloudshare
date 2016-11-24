'use strict';
import React, { Component, PropTypes } from 'react';

import { Card, Button, Input, Form, DatePicker } from 'antd';
import enUS from 'antd/lib/date-picker/locale/en_US';


const dateValueFormat = (dateString) => {
  let date = new Date(dateString),
      localDateString = date.toLocaleDateString(),
      splitDate = localDateString.split('/');
  splitDate.unshift(splitDate.splice(-1, 1));
  return splitDate.join('-');
};

class ResumeFollowUp extends Component {

  constructor() {
    super();

    this.state = {
      visible: false,
    };

    this.handleFocus = this.handleFocus.bind(this);
    this.handleFold = this.handleFold.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleFocus() {
    this.setState({
      visible: true,
    });
  }

  handleFold() {
    this.setState({
      visible: false,
    });
  }

  handleSubmit() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        console.log(errors);
        return;
      }
      values.date = dateValueFormat(values.date);
      this.props.onSubmitFollowUp(values);
    });
    this.props.form.resetFields();
  }

  render() {
    const { getFieldProps } = this.props.form;

    const customLocale = {
      timezoneOffset: 8 * 60,
      firstDayOfWeek: 0,
      minimalDaysInFirstWeek: 1,
    };

    return (
      <Card
        title="Follow Up"
        className="mg-t-8"
      >
        <Form className="bd-b-dotted">
          <Form.Item>
            <Input
              {...getFieldProps('text', {
                rules: [ { required: true }],
              })}
              type="text"
              placeholder="Please input content."
              size="small"
              onFocus={this.handleFocus}
            />
          </Form.Item>
          <div style={{ display: this.state.visible ? 'block' : 'none' }}>
            <Form.Item>
              <DatePicker
                {...getFieldProps('date')}
                style={{ width: '100%' }}
                size="small"
                locale={{ ...enUS, ...customLocale }}
                format="yyyy-MM-dd"
              />
            </Form.Item>
            <Form.Item>
              <a href="javascript:;" onClick={this.handleFold}>Fold</a>
              <Button type="ghost" size="small" className="submit-btn" onClick={this.handleSubmit}>Submit</Button>
            </Form.Item>
          </div>
        </Form>
        {this.props.dataSource.length > 0 ? 
          <div className="contend-box">
            {this.props.dataSource.map((item, index) => {
              return (
                <div key={index} className="content-item">
                  <em>{item.author} / {item.content.date}</em>
                  <p>{item.content.text}</p>
                </div>
              )
            })}
          </div>
          : ''}
      </Card>
    );
  }
}

export default ResumeFollowUp = Form.create({})(ResumeFollowUp);

ResumeFollowUp.propTypes = {
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      content: PropTypes.shape({
        text: PropTypes.string,
        date: PropTypes.string,
      })
    })
  ),
  onSubmitFollowUp: PropTypes.func,
};
