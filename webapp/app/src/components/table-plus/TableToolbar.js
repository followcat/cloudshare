'use strict';
import React, { Component, PropTypes } from 'react';
import { Row, Col, Input } from 'antd';

class TableToolbar extends Component {
  constructor() {
    super();
    this.handleSearchChange = this.handleSearchChange.bind(this);
  }

  handleSearchChange(e) {
    this.props.onSearch(e.target.value);
  }

  render() {
    const props = this.props;

    return (
      <Row className={`${props.prefixCls}`}>
        {(props.isSearched)
          ? <Col {...props.searchCol}>
              <Input
                placeholder={props.searchPlaceholder}
                onChange={this.handleSearchChange}
              />
            </Col>
          : null
        }
        {props.render.map((item, index) => {
          return (
            <Col key={index}>{item}</Col>
          );
        })}
      </Row>
    );
  }
}

TableToolbar.defaultProps = {
  prefixCls: 'cs-table-toolbar',
  isSearched: false,
  searchCol: {
    span: 6,
  },
  searchPlaceholder: "search",
  render: [],
  onSearch() {},
};

TableToolbar.propTypes = {
  prefixCls: PropTypes.string,
  isSearched: PropTypes.bool,
  searchCol: PropTypes.object,
  searchPlaceholder: PropTypes.string,
  render: PropTypes.array,
  onSearch: PropTypes.func,
};

export default TableToolbar;
