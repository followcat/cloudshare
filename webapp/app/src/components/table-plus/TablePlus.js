'use strict';
import React, { Component, PropTypes } from 'react';
import TableToolbar from './TableToolbar';
import { Table } from 'antd';

class TablePlus extends Component {
  constructor() {
    super();
    this.state = {
      filterData: [],
      search: '',
    };
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleSearch(value) {
    this.setState({
      search: value,
    });
  }

  render() {
    const props = this.props;
    let classes = props.prefixCls;

    if (props.className) {
      classes += props.className;
    }

    return (
      <div className={classes}>
        {(props.toolbar)
          ? <TableToolbar
              search={props.search}
              searchCol={props.searchCol}
              searchPlaceholder={props.searchPlaceholder}
              render={props.render}
              onSearch={this.handleSearch}
            />
          : null
        }
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
      </div>
    );
  }
}

TablePlus.defaultProps = {
  prefixCls: 'cs-table',
  className: '',
  toolbar: false,
  columns: [],
  rowSelection: {},
  size: 'default',
  loading: false,
  bordered: false,
  expandedRowKeys: [],
  onChange() {},
  onRowClick() {},
};

TablePlus.propTypes = {
  prefixCls: PropTypes.string,
  className: PropTypes.string,
  toolbar: PropTypes.bool,
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

export default TablePlus;
