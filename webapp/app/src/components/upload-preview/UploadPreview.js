'use strict';
import React, { Component, PropTypes } from 'react';
import PreviewWrapper from './PreviewWrapper';
import PreviewTopBar from './PreviewTopBar';
import PreviewTopBarForm from './PreviewTopBarForm';
import VersionPrompt from './VersionPrompt';
import Summary from '../summary';
import ResumeContent from '../resume-content';
import { Form } from 'antd';

class UploadPreview extends Component {
  render() {
    const props = this.props;

    return (
      <PreviewWrapper
        actived={props.currentPreview === props.index}
      >
        <PreviewTopBar
          form={props.form}
          id={props.id}
          currentPreview={props.currentPreview}
          total={props.total}
          onPrevClick={props.onPrevClick}
          onNextClick={props.onNextClick}
        >
          <PreviewTopBarForm
            form={props.form}
            id={props.id}
            resumeID={props.resumeID}
            name={props.name}
            currentPreview={props.currentPreview}
            total={props.total}
            classifyValue={props.classifyValue}
            classifyList={props.classifyList}
            confirmLoading={props.confirmLoading}
            onConfirmClick={props.onConfirmClick}
          />
        </PreviewTopBar>
        <VersionPrompt
          dataSource={props.similarResume}
        />
        <Summary 
          dataSource={props.summary}
        />
        <ResumeContent
          html={props.html}
        />
      </PreviewWrapper>
    );
  }
}

UploadPreview.defaultProps = {
  name: '',
  classifyValue: [],
  similarResume: [],
  summary: [],
  html: '',
  currentPreview: 0,
  total: 0,
  confirmLoading: false,
  onPrevClick() {},
  onNextClick() {},
  onConfirmClick() {},
};

UploadPreview.propTypes = {
  name: PropTypes.string,
  classifyValue: PropTypes.array,
  similarResume: PropTypes.array,
  summary: PropTypes.array,
  html: PropTypes.string,
  currentPreview: PropTypes.number,
  total: PropTypes.number,
  confirmLoading: PropTypes.bool,
  onPrevClick: PropTypes.func,
  onNextClick: PropTypes.func,
  onConfirmClick: PropTypes.func,
};

export default UploadPreview = Form.create({})(UploadPreview);
