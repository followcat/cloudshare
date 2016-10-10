'use strict';
import React, { Component } from 'react';

import { Row, Col, Pagination } from 'antd';

export default class SearchResultPagination extends Component {

  constructor(props) {
    super(props)
    this.state = {
      current: 1,
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(page) {
    this.setState({
      current: page,
    });
    this.props.onSwitchPage(page);
  }

  render() {
    return (
      <Row className="cs-search-result-bottom">
        <Col span={12} offset={12}>
          <Pagination
            showQuickJumper
            current={this.state.current}
            defaultCurrent={1}
            total={this.props.total}
            defaultPageSize={20}
            pageSize={20}
            onChange={this.handleChange}
          />
        </Col>
      </Row>
    );
  }
}