'use strict';
import React, { Component } from 'react';

import { Row, Col, Card, Checkbox, Button } from 'antd';

import WorkExperience from './WorkExperience';
import EducationExperience from './EducationExperience';

export default class SearchResultItem extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    const props = {...this.props};
    const education = props.yaml_info.education_history;
    const experience = props.yaml_info.experience;

    const current = props.yaml_info.current ? props.yaml_info.current : {},
          currentMoney = current.salary ? current.salary.yearly : '',
          currentPlacesList = current.places ? current.places : [];

    const expectation = props.yaml_info.expectation ? props.yaml_info.expectation : {},
          expectationMoney = expectation.salary ? expectation.salary.yearly : '',
          expectationPlacesList = expectation.places ? expectation.places : [];

    return (
      <Card className="cs-ls-i">
        <div className="basic-info">
          <Row>
            <Col span={1}>
              <Checkbox />
            </Col>
            <Col span={4}>
              <a href={`/show/${props.cv_id}`} target="_blank">{props.yaml_info.name ? props.yaml_info.name : props.yaml_info.id}</a>
            </Col>
            <Col span={1}>{props.yaml_info.gender}</Col>
            <Col span={1}>{props.yaml_info.age}</Col>
            <Col span={2}>{props.yaml_info.marital_status}</Col>
            <Col span={3}>{props.yaml_info.education}</Col>
            <Col span={3}>{props.yaml_info.school}</Col>
            <Col span={3}>{props.yaml_info.position}</Col>
            <Col span={3}>{props.yaml_info.company}</Col>
            <Col span={3}>{props.info.author}</Col>
          </Row>
        </div>
        <div className="extend-info">
          <Row gutter={16}>
            <Col span={18}>
              <EducationExperience education={education}/>
              <WorkExperience experience={experience}/>
            </Col>

            <Col span={6}>
              <div>Current:</div>
              <Row className="extend-info-r-row" gutter={8}>
                <Col className="extend-info-label" span={4}>
                  <label>Money:</label>
                </Col>
                <Col span={20}>{currentMoney}</Col>
              </Row>
              <Row className="extend-info-r-row" gutter={8}>
                <Col className="extend-info-label" span={4}>
                  <label>Place:</label>
                </Col>
                <Col span={20}>{currentPlacesList.join('')}</Col>
              </Row>

              <div>Expectation:</div>
              <Row className="extend-info-row" gutter={8}>
                <Col className="extend-info-label" span={4}>
                  <label>Money:</label>
                </Col>
                <Col span={20}>{expectationMoney}</Col>
              </Row>
              <Row className="extend-info-row" gutter={8}>
                <Col className="extend-info-label" span={4}>
                  <label>Place:</label>
                </Col>
                <Col span={20}>{expectationPlacesList}</Col>
              </Row>
            </Col>
          </Row>
        </div>
      </Card>
    );
  }
}