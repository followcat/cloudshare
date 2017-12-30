'use strict';
import React, { Component, PropTypes } from 'react';

import { Card } from 'antd';

import { URL } from 'URL';

import websiteText from 'config/website-text';

import DrawChart from './DrawChart';

const language = websiteText.zhCN;

class ResumeJobRecommend extends Component {

  constructor(props) {
    super(props);
    this.state = {
      visible: false,
      jdId: null
    }
    this.handleClickMore = this.handleClickMore.bind(this);
    this.getDomRader = this.getDomRader.bind(this);
  }

  handleClickMore(id) {
    this.setState({
      visible: true,
      jdId: id
    })
  }

  getDomRader() {
    return (
      <DrawChart resumeId={this.props.id} visible={this.state.visible} jdId={this.state.jdId}/>
    )
  }

  render() {
    return (
      <Card
        title={language.RESUME_JOB_RECOMMEND}
        className="mg-t-8"
        extra={
        <a
          onClick={this.handleClickMore}
        >
          {language.MORE}
        </a>
        }
      >
        <div className="recommend">
          {this.props.dataSource.map((item, index) => {
            return (
              <div key={index} className="recommend-item">
                <a onClick= {() =>{this.handleClickMore(item.id)}}>
                  {item.yaml_info.name ? item.yaml_info.name : item.id}
                  {item.yaml_info.company_name ? ' | ' + item.yaml_info.company_name: ''}
                </a>
              </div>
            );
          })}
        </div>
        {this.getDomRader()}
      </Card>
    );
  }
}

ResumeJobRecommend.propTypes = {
  dataSource: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string,
      yaml_info: PropTypes.shape({
        name: PropTypes.string,
        position: PropTypes.string,
        age: PropTypes.string,
        gender: PropTypes.string,
        education: PropTypes.string,
      }),
    })
  ),
};

export default ResumeJobRecommend;
