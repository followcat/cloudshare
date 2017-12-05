'use strict';
import React, { Component, PropTypes } from 'react';

import PreviewWrapper from './PreviewWrapper';
import ResumeContent from 'components/resume-content';
import ResumeTemplate from 'components/resume-template';

import { Form, Tabs } from 'antd';

class UploadPreview extends Component {
  render() {
    const {
      currentPreview,
      dataSource,
      index,
      html,
      children
    } = this.props;

    return (
      <PreviewWrapper
        actived={currentPreview === index}
      >
        {children}
      <Tabs defaultActiveKey="chinese">
        <Tabs.TabPane tab="中文" key="chinese">
          <ResumeTemplate dataSource={dataSource} />
        </Tabs.TabPane>
        <Tabs.TabPane tab="原文" key="html">
          <ResumeContent html={html} />
        </Tabs.TabPane>
      </Tabs>
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
