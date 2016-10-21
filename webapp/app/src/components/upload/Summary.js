'usr strict';
import React, { Component } from 'react';

import { Row, Col, Card } from 'antd';

export default class Summary extends Component {

  constructor(props) {
    super(props);

    this.getCompanyNameById = this.getCompanyNameById.bind(this);
  }

  getCompanyNameById(companyList, id) {
    for (let i = 0, len = companyList.length; i < len; i++) {
      if (companyList[i].id === id) {
          return companyList[i].name;
        }
    }
    return '';
  }


  render() {
    const props = this.props.dataSource,
          workExperience = props.experience.position ? props.experience.position : [],
          companyList = props.experience.company ? props.experience.company : [];

    return (
      <Card
        title="Summary"
      >
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
              <label>Education: </label>
            </Col>
            <Col span={16}>
              <span>{props.education}</span>
            </Col>
          </Col>
        </Row>
        <Row>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>University: </label>
            </Col>
            <Col span={16}>
              <span>{props.school}</span>
            </Col>
          </Col>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Position: </label>
            </Col>
            <Col span={16}>
              <span>{props.position}</span>
            </Col>
          </Col>
        </Row>
        <Row>
          <Col span={12}>
            <Col span={8} className="summary-label">
              <label>Company: </label>
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
              <span>{props.company}</span>
            </Col>
          </Col>
        </Row>
        <Row>
          <Col span={4} className="summary-label">
            <label>Education Experience: </label>
          </Col>
          <Col span={20}>
            {props.education_history.map(item => {
              return (
                <div>{item.date_from} - {item.date_to} | {item.education} | {item.major} | {item.school}</div>
              );
            })}
          </Col>
        </Row>
        <Row>
          <Col span={4} className="summary-label">
            <label>Work Experience: </label>
          </Col>
          <Col span={20}>
            {workExperience.map(item => {
              return (
                <div>{item.date_from} - {item.date_to} | {item.name} | {this.getCompanyNameById(companyList, item.at_company)} | {item.duration}</div>
              );
            })}
          </Col>
        </Row>
      </Card>
    );
  }
}