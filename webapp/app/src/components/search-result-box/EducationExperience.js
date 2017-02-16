'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col } from 'antd';

class EducationExperience extends Component {
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
      visible: !this.state.visible
    });
  }

  getExperienceDOMRender() {
    const { foldText, unfoldText } = this.props,
          { visible } = this.state;

    const education = this.props.education,
          len = education.length,
          isMoreThanTwo = len - 1 >= 2 ? true : false;  //判断需要折叠的部分是否大于两个条目

    const renderDOM = education.map((item, index) => {
      if (isMoreThanTwo) {
        if (index < 1) {  //第一个条目不需要折叠
          return (
            <div key={index}>{item.date_from}-{item.date_to} | {item.school} | {item.major} | {item.education}</div>
          );
        } else {  //除了第一个条目, 其它条目折叠
          return (
            <div key={index} className={visible ? 'showed' : 'hidden'}>
              {item.date_from}-{item.date_to} | {item.school} | {item.major} | {item.education}
            </div>
          );
        }
      } else {
        return (
          <div key={index}>{item.date_from}-{item.date_to} | {item.school} | {item.major} | {item.education}</div>
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
          <label>{`${this.props.educationExperienceText}: `}</label>
        </Col>
        <Col span={20}>
          {this.getExperienceDOMRender()}
        </Col>
      </Row>
    );
  }
}

EducationExperience.defaultProps = {
  educationExperienceText: 'Education Experience',
  education: [],
  foldText: 'Fold',
  unfoldText: 'Unfold'
};

EducationExperience.propTypes = {
  educationExperienceText: PropTypes.string,
  education: PropTypes.array,
  foldText: PropTypes.string,
  unfoldText: PropTypes.string
};

export default EducationExperience;
