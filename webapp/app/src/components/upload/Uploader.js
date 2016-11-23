import React, { Component, PropTypes } from 'react';

import { Upload, Icon } from 'antd';
const Dragger = Upload.Dragger;

export default class Uploader extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div style={{ width: 720, minHeight: 180, margin: '0 auto' }}>
          <Dragger 
            {...this.props.uploadProps}
            fileList={this.props.fileList}
          >
            <p className="ant-upload-drag-icon">
              <Icon type="inbox" />
            </p>
            <p className="ant-upload-text">Click or drag and drop files to upload on this area</p>
            <p className="ant-upload-hint">Support single or mutiple upload</p>
          </Dragger>
        </div>
      </div>
    );
  }
}

Uploader.propTypes = {
  uploadProps: PropTypes.object,
};