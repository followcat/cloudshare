'usr strict';
import React, { Component, PropTypes } from 'react';

import { Row, Col, Card } from 'antd';

import './summary.less';

export default class Summary extends Component {

  constructor(props) {
    super(props);

    this.getCompanyNameById = this.getCompanyNameById.bind(this);
  }

  getCompanyNameById(companyList, id) {
    let name = '';
    for (let i = 0, len = companyList.length; i < len; i++) {
      if (companyList[i].id === id) {
        name = companyList[i].name;
      }
    }
    return name;
  }


  render() {
    const props = this.props.dataSource;

    let workExperience = [],
        companyList = [],
        educationExperience = props.education_history ? props.education_history : [];

    if (props.experience) {
      workExperience = props.experience.hasOwnProperty('position') ? props.experience.position : [],
      companyList = props.experience.hasOwnProperty('company') ? props.experience.company : [];
    }

    return (
      <Card style={this.props.style}>
        <Row>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Name: </label>
            </Col>
            <Col span={16}>
              <span>{props.name}</span>
            </Col>
          </Col>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Gender: </label>
            </Col>
            <Col span={16}>
              <span>{props.gender}</span>
            </Col>
          </Col>
        </Row>
        <Row>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Age: </label>
            </Col>
            <Col span={16}>
              <span>{props.age}</span>
            </Col>
          </Col>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Marital Status: </label>
            </Col>
            <Col span={16}>
              <span>{props.marital_status}</span>
            </Col>
          </Col>
        </Row>
        <Row>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Education: </label>
            </Col>
            <Col span={16}>
              <span>{props.education}</span>
            </Col>
          </Col>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>University: </label>
            </Col>
            <Col span={16}>
              <span>{props.school}</span>
            </Col>
          </Col>
        </Row>
        <Row>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Position: </label>
            </Col>
            <Col span={16}>
              <span>{props.position}</span>
            </Col>
          </Col>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Company: </label>
            </Col>
            <Col span={16}>
              <span>{props.company}</span>
            </Col>
          </Col>
        </Row>
        <Row>
          <Col span={6} className="summary-label">
            <label>Education Experience: </label>
          </Col>
          <Col span={18}>
            {educationExperience.map((item, index) => {
              return (
                <div key={index}>{item.date_from} - {item.date_to} | {item.education} | {item.major} | {item.school}</div>
              );
            })}
          </Col>
        </Row>
        <Row>
          <Col span={6} className="summary-label">
            <label>Work Experience: </label>
          </Col>
          <Col span={18}>
            {workExperience.map((item, index) => {
              return (
                <div key={index}>{item.date_from} - {item.date_to} | {item.name} | {this.getCompanyNameById(companyList, item.at_company)} | {item.duration}</div>
              );
            })}
          </Col>
        </Row>
      </Card>
    );
  }
}

Summary.propTypes = {
  style: PropTypes.object,
  dataSource: PropTypes.shape({
    name: PropTypes.string,
    gender: PropTypes.string,
    age: PropTypes.string,
    marital_status: PropTypes.string,
    education: PropTypes.string,
    school: PropTypes.string,
    position: PropTypes.string,
    company: PropTypes.string,
    experience: PropTypes.shape({
      position: PropTypes.arrayOf(
        PropTypes.shape({
          at_company: PropTypes.number,
          date_from: PropTypes.string,
          date_to: PropTypes.string,
          duration: PropTypes.string,
          name: PropTypes.string,
        })
      ),
      company: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.number,
          date_from: PropTypes.string,
          date_to: PropTypes.string,
          duration: PropTypes.string,
          name: PropTypes.string,
        })
      ),
    }),
    education_history: PropTypes.arrayOf(
      PropTypes.shape({
        date_from: PropTypes.string,
        date_to: PropTypes.string,
        education: PropTypes.string,
        major: PropTypes.string,
        school: PropTypes.string,
      })
    )
  })
};
