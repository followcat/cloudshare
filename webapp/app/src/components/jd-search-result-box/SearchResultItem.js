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
      foldText,
      unfoldText,
      dataSource
    } = this.props;

    const description = dataSource.data.description;

    const name = dataSource.data.name ? dataSource.data.name : '',
          company = dataSource.data.company ? dataSource.data.company : '';

    const linkColor = gradient ? { color: gradient[parseInt(dataSource.value*100)] } : {};

    return (
      <Card className="cs-ls-i">
        <div className="basic-info">
          <Row>
            {type === 'default' ?
              null : 
              <Col span={0}>
                <Checkbox
                  data-id={dataSource[2].id}
                  data-name={dataSource[2].name}
                  onChange={this.handleCheckboxChange}
                  checked={findIndex(selection, (o) => o.id === yaml_info.id) > - 1 ? true : false}
                />
              </Col>
            }
            <Col span={5} className="omit name" >
              <a
                href={`/jd/${dataSource.id}`}
                style={linkColor}
                target="_blank"
              >
                {name}
            </a>
            </Col>
            <Col span={13} className="omit">
              <a
                href={`/company/${dataSource.data.companyID}`}
                style={linkColor}
                target="_blank"
              >
              {company}
              </a>
            </Col>
            <Col span={3} className="omit" style={linkColor}>{parseInt(dataSource.value*100)}</Col>
          </Row>
        </div>
        <div className="extend-info">
          <Row>
            <Col span={24}>
            <pre>
            {description}
            </pre>
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
