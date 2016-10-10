'use strict';
import React, { Component } from 'react';

import { Row, Col, Form, Input, Button } from 'antd';

export default class KeywordSearch extends Component {

  constructor() {
    super();
  }

  render() {
    return (
      <div className="center">
        <Row>
          <Col span={12} offset={6}>
            <Input id="sInput" size="large" />
          </Col>
        </Row>
        <Row>
          <Col span={4} offset={10}>
            <Button id="sBtn" type="primary" size="large">Search</Button>
          </Col>
        </Row>
      </div>
    );
  }
}