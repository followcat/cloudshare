'use strict';
import React, { Component, PropTypes } from 'react';

import PreviewWrapper from './PreviewWrapper';
import ResumeContent from 'components/resume-content';

import { Form } from 'antd';

class UploadPreview extends Component {
  render() {
    const {
      currentPreview,
      index,
      html,
      children
    } = this.props;

    return (
      <PreviewWrapper
        actived={currentPreview === index}
      >
        {children}
        <ResumeContent
          html={html}
        />
      </PreviewWrapper>
    );
  }
}

UploadPreview.defaultProps = {
  html: '',
  currentPreview: 0,
  index: 0
};

UploadPreview.propTypes = {
  html: PropTypes.string,
  currentPreview: PropTypes.number,
  index: PropTypes.number,
  children: PropTypes.arrayOf(PropTypes.element)
};

export default UploadPreview = Form.create({})(UploadPreview);
