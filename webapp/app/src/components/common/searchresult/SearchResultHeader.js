'use strict';
import React, { Component } from 'react';

import { Row, Col } from 'antd';

export default class SearchResultHeader extends Component {
  
  render() {
    return (
      <div className="cv-search-result-header">
        <Row>
          <Col className="header-cell" span={4}>Name</Col>
          <Col className="header-cell" span={2}>Gender</Col>
          <Col className="header-cell" span={1}>Age</Col>
          <Col className="header-cell" span={2}>Marriage</Col>
          <Col className="header-cell" span={3}>Education</Col>
          <Col className="header-cell" span={3}>University</Col>
          <Col className="header-cell" span={3}>Position</Col>
          <Col className="header-cell" span={3}>Company</Col>
          <Col className="header-cell" span={3}>Uploader</Col>
        </Row>
      </div>
    );
  }
}