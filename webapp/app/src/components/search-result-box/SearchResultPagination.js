'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Row,
  Col,
  Pagination
} from 'antd';

class SearchResultPagination extends Component {
  constructor() {
    super();
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(page) {
    this.props.onSwitchPage(page);
  }

  render() {
    const { current, pages, total } = this.props;
    const pageSize = 20;
    return (
      <Row className="cs-search-result-bottom">
        <Col span={12} offset={12}>
          <Pagination
            showQuickJumper
            current={current}
            defaultCurrent={1}
            total={pages*pageSize}
            defaultPageSize={pageSize}
            pageSize={pageSize}
            onChange={this.handleChange}
          />
        </Col>
      </Row>
    );
  }
}

SearchResultPagination.defaultProps = {
  onSwitchPage() {}
};

SearchResultPagination.propTypes = {
  current: PropTypes.number,
  total: PropTypes.number,
  onSwitchPage: PropTypes.func
};

export default SearchResultPagination;
