'use strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col } from 'antd';

export default class EducationExperience extends Component {

  constructor(props) {
    super(props);
    this.state = {
      visible: false,
      foldText: 'Unfold',
    };

    this.renderExperienceDOM = this.renderExperienceDOM.bind(this);
    this.handleFold = this.handleFold.bind(this);
  }

  renderExperienceDOM() {
    const education = this.props.education,
          len = education.length,
          isMoreThanTwo = len - 1 >= 2 ? true : false;  //判断需要折叠的部分是否大于两个条目

    const renderDOM = education.map((item, index) => {
      if (isMoreThanTwo) {
        if (index < 1) {  //第一个条目不需要折叠
          return (
            <div key={index}>{item.date_from}-{item.date_to} | {item.school} | {item.major} | {item.education}</div>
          )
        } else {  //除了第一个条目, 其它条目折叠
          return (
            <div key={index} className={this.state.visible ? 'showed' : 'hidden'}>
            {item.date_from}-{item.date_to} | {item.school} | {item.major} | {item.education}
            </div>
          )
        }
      } else {
        return (
          <div key={index}>{item.date_from}-{item.date_to} | {item.school} | {item.major} | {item.education}</div>
        )
      }
    });

    if (isMoreThanTwo) {
      return (
        <div>
        {renderDOM}
        <a href="javascript: void(0);" onClick={this.handleFold}>{this.state.foldText}</a>
        </div>
      )
    } else {
      return renderDOM;
    }
  }

  handleFold() {
    if (this.state.visible) {
      this.setState({
        visible: false,
        foldText: 'Unfold',
      });
    } else {
      this.setState({
        visible: true,
        foldText: 'Fold',
      });
    }
  }

  render() {
    return (
      <Row className="extend-info-l-row" gutter={8}>
        <Col className="extend-info-label" span={4}>
          <label>Education Experience:</label>
        </Col>
        <Col span={20}>
          {this.renderExperienceDOM()}
        </Col>
      </Row>
    );
  }
}

EducationExperience.propTypes = {
  education: PropTypes.array,
};