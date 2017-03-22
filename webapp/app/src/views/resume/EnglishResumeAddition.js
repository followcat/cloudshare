'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Button,
  Modal,
  Upload,
  Icon,
  message
} from 'antd';

import { confirmUpload } from 'request/upload';

import { API } from 'API';

import StorageUtil from 'utils/storage';

class EnglishResumeAddition extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      fileList: []
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleModalOk = this.handleModalOk.bind(this);
    this.handleUploadChange = this.handleUploadChange.bind(this);
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

  handleModalOk() {
    const { resumeId } = this.props;

    this.setState({
      loading: true
    });

    confirmUpload(API.UPLOAD_ENGLISH_RESUME_API, {
      id: resumeId
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200 && json.data.en_html) {
        this.setState({
          loading: false,
          fileList: [],
          enHtml: json.data.en_html,
        });
      } else {
        this.setState({
          loading: false,
          fileList: [],
        });
        message.error('上传英文简历失败.');
      }
    });
  }

  handleUploadChange(info) {
    let fileList = info.fileList;
    fileList = fileList.map((file) => {
      if (file.response) {
        file.url = file.response.data.url;
      }
      return file;
    });
    if (info.file.status === 'done') {
      message.success(`上传${info.file.name}成功.`);
    } else if (info.file.status === 'error') {
      message.error(`上传${info.file.name}失败.`);
    }

    this.setState({ fileList });
  }

  render() {
    const { visible, loading, fileList } = this.state;

    const uploadProps = {
      name: 'file',
      action: API.UPLOAD_ENGLISH_RESUME_API,
      headers: {
        Authorization: `Basic ${StorageUtil.get('token')}`,
      },
      onChange: this.handleUploadChange,
    };

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
          confirmLoading={loading}
          okText="确认"
          onOk={this.handleModalOk}
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
  style: PropTypes.object,
  enComfirmLoading: PropTypes.bool,
  upload: PropTypes.object,
  fileList: PropTypes.array,
  onEnComfirmLoading: PropTypes.func
};

EnglishResumeAddition.propTypes = {
  resumeId: PropTypes.string
};

export default EnglishResumeAddition;
