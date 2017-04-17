'use strict';
import React, { Component, PropTypes } from 'react';
import { Upload, Icon } from 'antd';
const Dragger = Upload.Dragger;

class DraggerUpload extends Component {
  render() {
    const {
      prefixCls,
      name,
      fileList,
      action,
      headers,
      multiple,
      accept,
      disabled,
      beforeUpload,
      text,
      hint
    } = this.props;

    return (
      <div className={prefixCls}>
        <Dragger
          name={name}
          fileList={fileList}
          action={action}
          headers={headers}
          multiple={multiple}
          accept={accept}
          onChange={this.props.onChange}
          onRemove={this.props.onRemove}
          disabled={disabled}
          beforeUpload={beforeUpload}
        >
          <p className="ant-upload-drag-icon">
            <Icon type="inbox" />
          </p>
          <p className="ant-upload-text">{text}</p>
          <p className="ant-upload-hint">{hint}</p>
        </Dragger>
      </div>
    );
  }
}

DraggerUpload.defaultProps = {
  prefixCls: 'cs-upload',
  name: 'file',
  text: '',
  hint: '',
  disabled: false,
};

DraggerUpload.propTypes = {
  prefixCls: PropTypes.string,
  name: PropTypes.string,
  fileList: PropTypes.arrayOf(PropTypes.object),
  action: PropTypes.string,
  headers: PropTypes.object,
  multiple: PropTypes.bool,
  accept: PropTypes.string,
  beforeUpload: PropTypes.func,
  onChange: PropTypes.func,
  onRemove: PropTypes.func,
  disabled: PropTypes.bool,
  text: PropTypes.string,
  hint: PropTypes.string,
};

export default DraggerUpload;
