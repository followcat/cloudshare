'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Button,
  Modal,
  Upload,
  Icon
} from 'antd';

class EnglishResumeAddition extends Component {
  constructor() {
    super();
    this.state = {
      visible: false
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleClick() {
    this.setState({
      visible: true,
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  render() {
    const { visible } = this.state,
          { uploadProps, fileList, confirmLoading } = this.props;

    return (
      <div style={{ display: 'inline-block', marginLeft: 4 }}>
        <Button
          type="ghost"
          size="small"
          onClick={this.handleClick}
        >
          添加英文简历
        </Button>
        <Modal
          title="上传英文简历"
          visible={visible}
          confirmLoading={confirmLoading}
          okText="确认"
          onOk={this.props.onUploadModalOk}
          onCancel={this.handleCancel}
        >
          <Upload
            {...uploadProps}
            fileList={fileList}
          >
            <Button type="ghost">
              <Icon type="upload" /> 上传文件
            </Button>
          </Upload>
        </Modal>
      </div>
    );
  }
}

EnglishResumeAddition.propTypes = {
  confirmLoading: PropTypes.bool,
  uploadProps: PropTypes.object,
  fileList: PropTypes.array,
  onUploadModalOk: PropTypes.func
};

export default EnglishResumeAddition;
