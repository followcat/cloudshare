'use strict';
import React, { Component, PropTypes } from 'react';

import { deleteAdditionalInfo } from 'request/resume';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

import {
  Card,
  Form,
  Input,
  Button,
  message,
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

  handleTagClose = (tag) => {
    deleteAdditionalInfo({
      unique_id: this.props.uniqueId,
      update_info: {"tag": tag.content},
      date: tag.date,
    }, json => {
      if (json.code === 200) {
        message.success(language.DELETE_SUCCESS_MSG);
      } else {
        message.error(language.DELETE_FAIL_MSG);
      }
    });
  }

  handleSubmit() {
    const fieldValue = this.props.form.getFieldsValue();
    this.props.onSubmitTag(fieldValue);
    this.props.form.resetFields();
  }

  render() {
    const { getFieldDecorator } = this.props.form;
    const { uniqueId, dataSource } = this.props;
    return (
      <Card
        title="标签"
      >
        {dataSource.map((item, index) => {
          return (<Tag key={index} color="blue-inverse" size="small"
                    closable onClose={() => this.handleTagClose(item)}
                  >{item.content}</Tag>);
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
