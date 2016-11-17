'use strict';
import React, { Component, PropTypes } from 'react';
import { Table } from 'antd';

class TableContent extends Component {
  render() {
    const props = this.props;

    return (
      <Table
        dataSource={props.dataSource}
        columns={props.columns}
        rowSelection={props.rowSelection}
        pagination={props.pagination}
        size={props.pagination}
        loading={props.loading}
        bordered={props.bordered}
        expandedRowKeys={props.expandedRowKeys}
        onChange={props.onChange}
        onRowClick={props.onRowClick}
        scroll={props.scroll}
      />
    );
  }
}

TableContent.defaultProps = {
  dataSource: [],
  columns: [],
  rowSelection: {},
  size: 'default',
  loading: false,
  bordered: false,
  onChange() {},
  onRowClick() {},
};

TableContent.propTypes = {
  dataSource: PropTypes.array,
  columns: PropTypes.array,
  rowSelection: PropTypes.object,
  pagination: PropTypes.object,
  size: PropTypes.string,
  loading: PropTypes.bool,
  bordered: PropTypes.bool,
  expandedRowKeys: PropTypes.array,
  scroll: PropTypes.object,
  onChange: PropTypes.func,
  onRowClick: PropTypes.func,
};

export default TableContent;
