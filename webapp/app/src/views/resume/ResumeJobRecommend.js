'use strict';
import React, { Component, PropTypes } from 'react';

import { Card } from 'antd';

import { URL } from 'URL';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class ResumeJobRecommend extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Card
        title={language.RESUME_JOB_RECOMMEND}
        className="mg-t-8"
        extra={
        <a
          href={URL.getFastMatchingByCV(this.props.id)}
        >
         {language.MORE}
        </a>}
      >
        <div className="recommend">
          {this.props.dataSource.map((item, index) => {
            return (
              <div key={index} className="recommend-item">
                <a href={`/jd/${item.id}`}>
                  {item.yaml_info.name ? item.yaml_info.name : item.id}
                  {item.yaml_info.company_name ? ' | ' + item.yaml_info.company_name: ''}
                </a>
              </div>
            );
          })}
        </div>
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
