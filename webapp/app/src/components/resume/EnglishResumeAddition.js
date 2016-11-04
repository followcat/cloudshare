'use strict';
import React, { Component, PropTypes } from 'react';

import { Button, Modal, Upload, Icon } from 'antd';

export default class EnglishResumeAddition extends Component {

  constructor() {
    super();

    this.state = {
      visible: false,
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
    return (
      <div style={this.props.style}>
        <Button
          type="ghost"
          size="small"
          onClick={this.handleClick}
        >
          Add English CV
        </Button>
        <Modal
          title="English CV Uploader"
          visible={this.state.visible}
          confirmLoading={this.props.enComfirmLoading}
          okText="Confirm"
          onOk={this.props.onEnComfirmLoading}
          onCancel={this.handleCancel}
        >
          <Upload
            {...this.props.upload}
            fileList={this.props.fileList}
          >
            <Button type="ghost">
              <Icon type="upload" /> Upload File
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
  onEnComfirmLoading: PropTypes.func.isRequired,
};
