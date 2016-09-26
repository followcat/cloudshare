'use strict';
import React, { Component } from 'react';

import { Row, Col, Pagination } from 'antd';

export default class SearchResultPagination extends Component {
  render() {
    return (
      <Row className="cs-search-result-bottom">
        <Col span={12} offset={12}>
          <Pagination showQuickJumper defaultCurrent={1} total={500} />
        </Col>
      </Row>
    );
  }
}