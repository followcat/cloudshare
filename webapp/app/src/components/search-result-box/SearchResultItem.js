'use strict';
import React, { Component, PropTypes } from 'react';

import WorkExperience from './WorkExperience';
import EducationExperience from './EducationExperience';

import {
  Row,
  Col,
  Card,
  Checkbox
} from 'antd';

import findIndex from 'lodash/findIndex';
import { generateWorkExperience } from 'utils/summary-generator';

class SearchResultItem extends Component {
  constructor() {
    super();
    this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
    this.getNameTextRender = this.getNameTextRender.bind(this);
  }

  handleCheckboxChange(e) {
    this.props.onToggleSelection({
      id: e.target['data-id'],
      name: e.target['data-name']
    });
  }

  getNameTextRender() {
    const { yaml_info } = this.props;
    const name = yaml_info.name ? yaml_info.name : yaml_info.id,
          origin = yaml_info.origin ? ' - ' + yaml_info.origin : '';
          if(name === "[*****]") {
            return 'id-'+yaml_info.id;
          }
    return name ;
  }

  render() {
    const {
      yaml_info,
      gradient,
      info,
      type,
      selection,
      cv_id,
      workExperienceText,
      educationExperienceText,
      foldText,
      unfoldText
    } = this.props;

    const education = yaml_info.education_history || [];
    const experience = yaml_info.experience;

    const current = yaml_info.current ? yaml_info.current : {},
          currentMoney = current.salary ? current.salary.yearly : '',
          currentPlacesList = current.places ? current.places : [];

    const expectation = yaml_info.expectation ? yaml_info.expectation : {},
          expectationMoney = expectation.salary ? expectation.salary.yearly : '',
          expectationPlacesList = expectation.places ? expectation.places : [];

    const linkColor = gradient ? { color: gradient[parseInt(info.match*100)] } : {};

    return (
      <Card className="cs-ls-i">
        <div className="basic-info">
          <Row>
            {type === 'default' ?
              null : 
              <Col span={1}>
                <Checkbox
                  data-id={yaml_info.id}
                  data-name={yaml_info.name}
                  onChange={this.handleCheckboxChange}
                  checked={findIndex(selection, (o) => o.id === yaml_info.id) > - 1 ? true : false}
                />
              </Col>
            }
            <Col span={type === 'default' ? 4 : 3} className="omit">
              <a
                href={`/resume/${cv_id}`}
                style={linkColor}
                target="_blank"
              >
                {this.getNameTextRender()}
              </a>
            </Col>
            <Col span={1} className="omit">{yaml_info.gender}</Col>
            <Col span={1} className="omit">{yaml_info.age}</Col>
            <Col span={2} className="omit">{yaml_info.marital_status}</Col>
            <Col span={3} className="omit">{yaml_info.education}</Col>
            <Col span={3} className="omit" title={yaml_info.school}>{yaml_info.school}</Col>
            <Col span={3} className="omit" title={yaml_info.position}>{yaml_info.position}</Col>
            <Col span={4} className="omit" title={yaml_info.company}>{yaml_info.company}</Col>
            <Col span={3} className="omit">{info.author ? info.author : 'null'}, {info.time.split(' ')[0].replace(/\-/g, '/')}</Col>
          </Row>
        </div>
        <div className="extend-info">
          <Row>
            <Col span={18}>
              <EducationExperience
                educationExperienceText={educationExperienceText}
                foldText={foldText}
                unfoldText={unfoldText}
                education={education}
              />
              <WorkExperience
                workExperienceText={workExperienceText}
                foldText={foldText}
                unfoldText={unfoldText}
                experience={generateWorkExperience(experience)}
              />
            </Col>
            <Col span={6}>
              <div>目前状态:</div>
              <Row className="extend-info-r-row">
                <Col className="extend-info-label" span={4}>
                  <label>薪酬:</label>
                </Col>
                <Col span={20}>{currentMoney}</Col>
              </Row>
              <Row className="extend-info-r-row">
                <Col className="extend-info-label" span={4}>
                  <label>地点:</label>
                </Col>
                <Col span={20}>{currentPlacesList.join('')}</Col>
              </Row>
              <div>期望状态:</div>
              <Row className="extend-info-row">
                <Col className="extend-info-label" span={4}>
                  <label>薪酬:</label>
                </Col>
                <Col span={20}>{expectationMoney}</Col>
              </Row>
              <Row className="extend-info-row">
                <Col className="extend-info-label" span={4}>
                  <label>地点:</label>
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

SearchResultItem.propTypes = {
  cv_id: PropTypes.string,
  workExperienceText: PropTypes.string,
  educationExperienceText: PropTypes.string,
  foldText: PropTypes.string,
  unfoldText: PropTypes.string,
  gradient: PropTypes.array,
  info: PropTypes.object,
  type: PropTypes.string,
  selection: PropTypes.array,
  yaml_info: PropTypes.shape({
    name: PropTypes.string,
    education_history: PropTypes.array,
    experience: PropTypes.object,
    current: PropTypes.object,
    gender: PropTypes.string,
    age: PropTypes.string,
    marital_status: PropTypes.string,
    education: PropTypes.string,
    school: PropTypes.string,
    position: PropTypes.string,
    company: PropTypes.string,
    author: PropTypes.string,
  }),
  onToggleSelection: PropTypes.func
};

export default SearchResultItem;
