'use strict';
import React, { Component, PropTypes } from 'react';
import { Row, Col, Input } from 'antd';

class TableToolbar extends Component {
  constructor() {
    super();
  }

  handleSearchChange(e) {
    this.props.onSearch(e.target.value);
  }

  render() {
    const props = this.props;

    return (
      <Row className={`${props.prefixCls}`}>
        {(props.search)
          ? <Col {...props.searchCol}>
              <Input
                searchPlaceholder={props.placeholder}
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
  search: false,
  searchCol: {
    span: 6,
  },
  searchPlaceholder: "search",
  render: [],
  onSearch() {},
};

TableToolbar.propTypes = {
  prefixCls: PropTypes.string,
  search: PropTypes.bool,
  searchCol: PropTypes.object,
  searchPlaceholder: PropTypes.string,
  render: PropTypes.array,
  onSearch: PropTypes.func,
};

export default TableToolbar;
