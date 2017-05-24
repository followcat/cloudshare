'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Card,
  Form,
  Input,
  Button
} from 'antd';

class ResumeComment extends Component {
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
      this.props.onSubmitComment(values);
    });
    this.props.form.resetFields();
  }

  render() {
    const { getFieldDecorator } = this.props.form,
          { dataSource } = this.props;

    return (
      <Card
        title="评论"
        className="mg-t-8"
      >
        <Form className="bd-b-dotted">
          <Form.Item>
            {getFieldDecorator('comment', {
              rules: [{ required: true }]
            })(
              <Input
                type="text"
                size="small"
                onFocus={this.handleFocus}
              />
            )}
          </Form.Item>
          <Form.Item style={{ display: this.state.visible ? 'block' : 'none' }}>
            <a href="javascript:;" onClick={this.handleFold}>折叠</a>
            <Button type="ghost" size="small" className="submit-btn" onClick={this.handleSubmit}>提交</Button>
          </Form.Item>
        </Form>
        {dataSource && dataSource.length > 0 ? 
          <div className="contend-box">
            {dataSource.map((item, index) => {
              return (
                <div key={index} className="content-item">
                  <em>{item.author} / {item.date}</em>
                  <p>{item.content}</p>
                </div>
              );
            })}
          </div>
          : ''}
      </Card>
    );
  }
}

ResumeComment.propTypes = {
  form: PropTypes.object,
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      author: PropTypes.string,
      date: PropTypes.string,
      content: PropTypes.string,
    })
  ),
  onSubmitComment: PropTypes.func,
};

export default ResumeComment = Form.create({})(ResumeComment);
