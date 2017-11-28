'use strict';
import React, { Component, PropTypes } from 'react';
import { Icon } from 'antd';

import WorkExperience from 'components/search-result-box/WorkExperience';
import EducationExperience from 'components/search-result-box/EducationExperience';

import Charts from './Charts';
import { getValuableData } from 'request/analyse';
import { getRadarOption } from 'utils/chart_option';

import classNames from 'classnames';

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
    var option = {
    title: { text: '正在分析' },
    tooltip: {},
    legend: { data: [] },
    radar: { indicator: [] },
    series: [{
        name: '',
        type: 'radar',
        data : []}]
    };
    this.state = {
      option: option,
      chartVisible: false,
      anonymized: false,
    };
    this.handleCheckboxChange = this.handleCheckboxChange.bind(this);
    this.getNameTextRender = this.getNameTextRender.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    const {
      cv_id,
      postData,
      addedChartResult,
    } = this.props;
    const { chartVisible } = this.state;

    getValuableData(Object.assign({}, {
        doc: postData.doc,
        name_list: [cv_id],
        uses: ['medical'],
      }), json => {
        if (json.code === 200) {
          json.data.result.forEach(function (item) {
            if (addedChartResult !== undefined) {
              addedChartResult.forEach(function (cresult) {
              cresult.forEach(function (critem) {
                if (critem['description'] === item['description']) {
                  item['value'] = item['value'].concat(critem['value']); }
                })
              })
            };
          });
          this.setState({
            data: json.data.result,
            option: getRadarOption(json.data.max,
                                   json.data.result,
                                   this.state.anonymized),
          });
        }
      });

    this.setState({
      option: {},
      chartVisible: !chartVisible,
    });
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
    return name + origin;
  }

  render() {
    const {
      prefixCls,
      yaml_info,
      gradient,
      info,
      type,
      cv_id,
      workExperienceText,
      educationExperienceText,
      foldText,
      unfoldText
    } = this.props,
    { option, chartVisible } = this.state;
    const classSet = classNames({
      [`${prefixCls}`]: true,
      'showed': chartVisible === true,
      'hidden': chartVisible === false,
    });

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
            <Col span={type === 'default' ? 3 : 4} className="omit">
              <a
                style={linkColor}
                onClick={this.handleClick}
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
            <Col span={7} className="omit" title={yaml_info.company}>{yaml_info.company}</Col>
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
          <div className={classSet}>
            <Charts
              option={option}
              style={{ width: 900, height: 460, margin: '0 auto' }} />
          </div>
        </div>
      </Card>
    );
  }
}

SearchResultItem.defaultProps = {
  prefixCls: 'cs-search-result'
};

SearchResultItem.propTypes = {
  cv_id: PropTypes.string,
  workExperienceText: PropTypes.string,
  educationExperienceText: PropTypes.string,
  foldText: PropTypes.string,
  unfoldText: PropTypes.string,
  gradient: PropTypes.array,
  info: PropTypes.object,
  type: PropTypes.string,
  addedChartResult: PropTypes.array,
  postData: PropTypes.object,
  yaml_info: PropTypes.shape({
    name: PropTypes.string,
    education_history: PropTypes.array,
    experience: PropTypes.object,
    current: PropTypes.object,
    gender: PropTypes.string,
    age: PropTypes.number,
    marital_status: PropTypes.string,
    education: PropTypes.string,
    school: PropTypes.string,
    position: PropTypes.string,
    company: PropTypes.string,
    author: PropTypes.string,
  }),
};

export default SearchResultItem;
