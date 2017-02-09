'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col } from 'antd';

export default class WorkExperience extends Component {

  constructor() {
    super();
    this.state = {
      visible: false
    };
    this.handleFold = this.handleFold.bind(this);
    this.getExperienceDOMRender = this.getExperienceDOMRender.bind(this);
  }

  handleFold() {
    this.setState({
      visible: !this.state.visible,
    });
  }

  getExperienceDOMRender() {
    const { foldText, unfoldText } = this.props,
          { visible } = this.state;

    const experience = this.props.experience,
          len = experience.length,
          isMoreThanTwo = len - 2 >= 2 ? true : false;  //判断需要折叠的部分是否大于两个条目

    const renderDOM = experience.map((item, index) => {
      if (isMoreThanTwo) {
        if (index < 2) {  //前两个条目不需要折叠
          return (
            <div key={index}>
              {item.date_from}-{item.date_to} | {item.business ? item.business + '|' : ''}{item.companyName ? item.companyName + '|' : ''} {item.name} | {item.duration}
            </div>
          );
        } else {  //除了前两个条目, 其它条目折叠
          return (
            <div key={index} className={visible ? 'showed' : 'hidden'}>
              {item.date_from}-{item.date_to} | {item.business ? item.business + '|' : ''}{item.companyName ? item.companyName + '|' : ''} {item.name} | {item.duration}
            </div>
          );
        }
      } else {
        return (
          <div key={index}>
            {item.date_from}-{item.date_to} | {item.business ? item.business + '|' : ''}{item.companyName ? item.companyName + '|' : ''} {item.name} | {item.duration}
          </div>
        );
      }
    });
    
    if (isMoreThanTwo) {
      return (
        <div>
          {renderDOM}
          <a href="javascript: void(0);" onClick={this.handleFold}>{visible ? unfoldText : foldText}</a>
        </div>
      );
    } else {
      return renderDOM;
    }
  }



  render() {
    return (
      <Row className="extend-info-l-row" gutter={8}>
        <Col className="extend-info-label" span={4}>
            <label>{`${this.props.workExperienceText}: `}</label> 
        </Col>
        <Col span={20}>
          {this.getExperienceDOMRender()}
        </Col>
      </Row>
    );
  }
}

WorkExperience.defaultProps = {
  workExperienceText: 'Work Experience',
  experience: [],
  foldText: 'Fold',
  unfoldText: 'Unfold'
};

WorkExperience.propTypes = {
  workExperienceText: PropTypes.string,
  experience: PropTypes.array,
  foldText: PropTypes.string,
  unfoldText: PropTypes.string
};