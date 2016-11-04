'use strict';
import React, { Component, PropTypes } from 'react';

import { Card, Form, Input, Button } from 'antd';

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
        console.log(errors);
        return;
      }
      this.props.onSubmitComment(values);
    });
  }

  render() {
    const { getFieldProps } = this.props.form;

    return (
      <Card
        title="Comments"
        className="mg-t-8"
      >
        <Form className="bd-b-dotted">
          <Form.Item>
            <Input
              {...getFieldProps('comment', {
                rules: [ { required: true }]
              })}
              type="text"
              placeholder="Please input content"
              size="small"
              onFocus={this.handleFocus}
            />
          </Form.Item>
          <Form.Item style={{ display: this.state.visible ? 'block' : 'none' }}>
            <a href="javascript:;" onClick={this.handleFold}>Fold</a>
            <Button type="ghost" size="small" className="submit-btn" onClick={this.handleSubmit}>Submit</Button>
          </Form.Item>
        </Form>
        {this.props.dataSource.length > 0 ? 
          <div className="contend-box">
            {this.props.dataSource.map((item, index) => {
              return (
                <div key={index} className="content-item">
                  <em>{item.author} / {item.date}</em>
                  <p>{item.content}</p>
                </div>
              )
            })}
          </div>
          : ''}
      </Card>
    )
  }
}

export default ResumeComment = Form.create({})(ResumeComment);

ResumeComment.propTypes = {
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      author: PropTypes.string,
      date: PropTypes.string,
      content: PropTypes.string,
    })
  ),
  onSubmitComment: PropTypes.func.isRequired,
};
