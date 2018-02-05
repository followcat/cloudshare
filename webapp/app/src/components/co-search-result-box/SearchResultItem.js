'use strict';
import React, { Component, PropTypes } from 'react';

import WorkExperience from './WorkExperience';
import EducationExperience from './EducationExperience';

import {
  Row,
  Col,
  Card,
  Tag,
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
      selection,
      cv_id,
      foldText,
      unfoldText,
      dataSource
    } = this.props;
    const name = dataSource.name ? dataSource.name : '',
          place = dataSource.place.length > 0 ? dataSource.place : '',
          employees = dataSource.total_employees ? dataSource.total_employees : '',
          type = dataSource.type ? dataSource.type : '',
          website = dataSource.website ? dataSource.website : '',
          description = dataSource.description ? dataSource.description : '';

    return (
      <Card className="cs-ls-i">
        <div className="basic-info">
          <Row>
            <Col span={4} className="omit name" >
              <a
                href={`/company/${dataSource.id}`}
                target="_blank"
              >
                {name}
            </a>
            </Col>
          </Row>
          <Row>
            <Col span={6} className="basic-info-tag" >
              {employees && <Tag>{employees}</Tag>}
              {type && <Tag>{type}</Tag>}
            </Col>
          </Row>
        </div>
        {description && <div className="extend-info">
          <Row>
            <Col span={24}>
            <p>{description}</p>
            </Col>
          </Row>
        </div>}
        <div className="project-info">

        { dataSource.project.map(item =>{
          return (
            <Row>
            <Col span={10}>
            <span>{item.date_from}-{item.date_to}</span>
            </Col>
            <Col span={10}>
            <span>{item.name}</span>
            </Col>
            </Row>
            )
          })
        }
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
