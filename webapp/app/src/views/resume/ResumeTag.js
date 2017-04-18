'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Card,
  Form,
  Input,
  Button,
  Tag
} from 'antd';

class ResumeTag extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleClick() {
    this.setState({
      visible: !this.state.visible,
    });
  }

  handleSubmit() {
    const fieldValue = this.props.form.getFieldsValue();
    this.props.onSubmitTag(fieldValue);
    this.props.form.resetFields();
  }

  render() {
    const { getFieldDecorator } = this.props.form;

    return (
      <Card
        title="标签"
      >
        {this.props.dataSource.map((item, index) => {
          return (<Tag key={index} color="blue-inverse" size="small">{item.content}</Tag>);
        })}
        <a
          style={{ display: 'block' }}
          href="javascript:;"
          onClick={this.handleClick}
        >
          {this.state.visible ? '折叠' : '新增标签'}
        </a>
        <Form layout="inline" style={{ display: this.state.visible ? 'block' : 'none' }}>
          <Form.Item>
            {getFieldDecorator('tag')(
              <Input size="small" />
            )}
          </Form.Item>
          <Form.Item>
            <Button type="ghost" size="small" onClick={this.handleSubmit}>提交</Button>
          </Form.Item>
        </Form>
      </Card>
    );
  }
}

ResumeTag.defaultProps = {
  dataSource: []
};

ResumeTag.propTypes = {
  form: PropTypes.object,
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      content: PropTypes.string,
    })
  ),
  onSubmitTag: PropTypes.func
};

export default ResumeTag = Form.create({})(ResumeTag);
