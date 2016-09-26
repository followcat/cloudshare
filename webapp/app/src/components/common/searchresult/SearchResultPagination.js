'use strict';
import React, { Component } from 'react';

import { Row, Col, Pagination } from 'antd';

export default class SearchResultPagination extends Component {

  constructor(props) {
    super(props)
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(page) {
    this.props.onSwitchPage(page);
  }

  render() {
    return (
      <Row className="cs-search-result-bottom">
        <Col span={12} offset={12}>
          <Pagination
            showQuickJumper
            defaultCurrent={1}
            total={this.props.total}
            onChange={this.handleChange}
          />
        </Col>
      </Row>
    );
  }
}