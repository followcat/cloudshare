'use strict';
import React, { Component, PropTypes } from 'react';

import { Card, Form, Input, Button, Tag } from 'antd';

class ResumeTag extends Component {

  constructor(props) {
    super(props);

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
    const { getFieldProps } = this.props.form;

    return (
      <Card
        title="Tag"
      >
        {this.props.dataSource.map((item, index) => {
          return (<Tag key={index} color="blue" size="small">{item.content}</Tag>)
        })}
        <a
          style={{ display: 'block' }}
          href="javascript:;"
          onClick={this.handleClick}
        >
          {this.state.visible ? 'Fold' : 'Add a tag'}
        </a>
        <Form inline style={{ display: this.state.visible ? 'block' : 'none' }}>
          <Form.Item>
            <Input
              {...getFieldProps('tag')}
              placeholder="Please input a tag name."
              size="small"
            />
          </Form.Item>
          <Form.Item>
            <Button type="ghost" size="small" onClick={this.handleSubmit}>Submit</Button>
          </Form.Item>
        </Form>
      </Card>
    )
  }
}

ResumeTag.defaultProps = {
  dataSource: []
};

ResumeTag.propTypes = {
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      content: PropTypes.string,
    })
  ),
  onSubmitTag: PropTypes.func.isRequired,
};

export default ResumeTag = Form.create({})(ResumeTag);
