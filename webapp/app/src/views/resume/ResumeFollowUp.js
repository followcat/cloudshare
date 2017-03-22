'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Card,
  Button,
  Input,
  Form,
  DatePicker
} from 'antd';

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
        return;
      }
      values['date'] = values['date'].format('YYYY-MM-DD');

      this.props.onSubmitFollowUp(values);
    });
    this.props.form.resetFields();
  }

  render() {
    const { getFieldDecorator } = this.props.form,
          { dataSource } = this.props;

    return (
      <Card
        title="跟进情况"
        className="mg-t-8"
      >
        <Form className="bd-b-dotted">
          <Form.Item>
            {getFieldDecorator('text', {
              rules: [{ required: true }]
            })(
              <Input type="text" size="small" onFocus={this.handleFocus} />
            )}
          </Form.Item>
          <div style={{ display: this.state.visible ? 'block' : 'none' }}>
            <Form.Item>
              {getFieldDecorator('date')(
                <DatePicker style={{ width: '100%' }} size="small" />
              )}
            </Form.Item>
            <Form.Item>
              <a href="javascript:;" onClick={this.handleFold}>折叠</a>
              <Button type="ghost" size="small" className="submit-btn" onClick={this.handleSubmit}>提交</Button>
            </Form.Item>
          </div>
        </Form>
        {dataSource && dataSource.length > 0 ? 
          <div className="contend-box">
            {dataSource.map((item, index) => {
              return (
                <div key={index} className="content-item">
                  <em>{item.author} / {item.content.date}</em>
                  <p>{item.content.text}</p>
                </div>
              );
            })}
          </div>
          : ''}
      </Card>
    );
  }
}

ResumeFollowUp.propTypes = {
  form: PropTypes.object,
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      content: PropTypes.shape({
        text: PropTypes.string,
        date: PropTypes.string,
      })
    })
  ),
  onSubmitFollowUp: PropTypes.func
};

export default ResumeFollowUp = Form.create({})(ResumeFollowUp);
