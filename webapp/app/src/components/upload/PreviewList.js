'use strict';
import React, { Component, PropTypes } from 'react';

import { Button, Icon } from 'antd';

import Preview from './Preview';
import ResumeTitle from './ResumeTitle';

import './previewlist.less';

export default class PreviewList extends Component {

  constructor(props) {
    super(props);
    this.isActive = this.isActive.bind(this);
  }

  isActive(index) {
    return index === this.props.currentPreview ? 'cs-preview cs-preview-active' : 'cs-preview';
  }

  render() {
    const previewListLength = this.props.previewList.length;
    return (
      <div>
        {this.props.previewList.map((previewItem, index) => {
          const resumeProps = {
            index: index,
            current: this.props.currentPreview,
            length: previewListLength,
            name: previewItem.name,
            id: previewItem.id,
            onPrevPreview: this.props.onPrevPreview,
            onNextPreview: this.props.onNextPreview,
            onComfirmUpload: this.props.onComfirmUpload,
            loading: this.props.loading,
            disabled: this.props.disabled,
            classifyList: this.props.classifyList,
          };

          return (
            <div key={index} className={this.isActive(index)}>
              <ResumeTitle {...resumeProps}/>
              <Preview markdown={previewItem.markdown} />
            </div>
          );
        })}
      </div>
    );
  }
}

PreviewList.propTypes = {
  previewList: PropTypes.array,
  currentPreview: PropTypes.number,
  loading: PropTypes.bool,
  disabled: PropTypes.bool,
  classifyList: PropTypes.array,
  onPrevPreview: PropTypes.func.isRequired,
  onNextPreview: PropTypes.func.isRequired,
  onComfirmUpload: PropTypes.func.isRequired,
};