'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon, Checkbox, Button, Tabs } from 'antd';

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
          <ResumeToolMenu
            dataSource={this.props.dataSource}
            upload={this.props.upload}
            fileList={this.props.fileList}
            enComfirmLoading={this.props.enComfirmLoading}
            onModifyTitle={this.props.onModifyTitle}
            onEnComfirmLoading={this.props.onEnComfirmLoading}
          />
          <Summary dataSource={this.props.dataSource} style={{ marginTop: 4 }} />
          <Tabs defaultActiveKey="1">
            <Tabs.TabPane
              tab="Chinese"
              key="1"
            >
              <ResumeContent html={this.props.html} />
            </Tabs.TabPane>
            <Tabs.TabPane
              tab="English"
              key="2"
              disabled={!this.props.enHtml}
            >
              <ResumeContent html={this.props.enHtml} />
            </Tabs.TabPane>
          </Tabs>
          
        </div>
      </div>
    );
  }
}

ResumeWrapper.propTypes = {
  collected: PropTypes.bool,
  dataSource: PropTypes.shape({
    id: PropTypes.string,
    origin: PropTypes.string,
    committer: PropTypes.string,
  }),
  upload: PropTypes.object,
  fileList: PropTypes.array,
  enComfirmLoading: PropTypes.bool,
  onModifyTitle: PropTypes.func.isRequired,
  onEnComfirmLoading: PropTypes.func.isRequired,
  html: PropTypes.string.isRequired,
  enHtml: PropTypes.string,
};
