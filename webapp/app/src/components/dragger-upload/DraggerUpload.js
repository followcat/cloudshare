'use strict';
import React, { Component, PropTypes } from 'react';
import { Upload, Icon } from 'antd';
const Dragger = Upload.Dragger;

class DraggerUpload extends Component {
  render() {
    const props = this.props;

    return (
      <div className={`${props.prefixCls}`}>
        <Dragger
          name={props.name}
          fileList={props.fileList}
          action={props.action}
          headers={props.headers}
          multiple={props.multiple}
          accept={props.accept}
          onChange={props.onChange}
          onRemove={props.onRemove}
          disabled={props.disabled}
        >
          <p className="ant-upload-drag-icon">
            <Icon type="inbox" />
          </p>
          <p className="ant-upload-text">{props.text}</p>
          <p className="ant-upload-hint">{props.hint}</p>
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
  onChange: PropTypes.func,
  onRemove: PropTypes.func,
  disabled: PropTypes.bool,
  text: PropTypes.string,
  hint: PropTypes.string,
};

export default DraggerUpload;
