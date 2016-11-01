'use strict';
import React, { Component } from 'react';

import { Icon, Checkbox, Button } from 'antd';

import ResumeToolMenu from './ResumeToolMenu';
import Summary from '../common/Summary';
import ResumeContent from '../common/ResumeContent';

export default class ResumeWrapper extends Component {

  constructor(props) {
    super(props);

    this.handleCollectClick = this.handleCollectClick.bind(this);
  }

  handleCollectClick() {
    this.props.onCollection();  //调用父组件方法
  }

  render() {
    return (
      <div className="cs-resume-wrapper">
        <div className="cs-resume-header">
          <div className="collect">
            <Icon
              type={this.props.collected ? 'star' : 'star-o'}
              style={this.props.collected ? { color: '#FFC107' } : {}}
              onClick={this.handleCollectClick}
            />
          </div>
          <div className="cs-resume-header-info">
            <label>ID: </label>
            <span>{this.props.dataSource.id}</span>
          </div>
          <div className="cs-resume-header-info">
            <label>Source: </label>
            <span>{this.props.dataSource.origin}</span>
          </div>
          <div className="cs-resume-header-info">
            <label>Uploader: </label>
            <span>{this.props.dataSource.committer}</span>
          </div>
        </div>
        <div className="cv-resume-content">
          <ResumeToolMenu onModifyTitle={this.props.onModifyTitle} dataSource={this.props.dataSource} />
          <Summary dataSource={this.props.dataSource} style={{ marginTop: 4 }} />
          <ResumeContent html={this.props.html} />
        </div>
      </div>
    );
  }
}