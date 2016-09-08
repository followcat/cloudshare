'use strict';
import React, { Component } from 'react';

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
    return (
      <div>
        {this.props.previewList.map((previewItem, index) => {
          const resumeProps = {
            index: index,
            current: this.props.currentPreview,
            length: this.props.length,
            yaml_info: previewItem.yaml_info,
            onPrevPreview: this.props.onPrevPreview,
            onNextPreview: this.props.onNextPreview,
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