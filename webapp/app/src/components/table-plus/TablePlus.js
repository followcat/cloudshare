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
    this.updateFilterData = this.updateFilterData.bind(this);
    this.getDataSource = this.getDataSource.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.dataSource.length !== this.props.dataSource.length) {
      this.updateFilterData(this.state.search, nextProps);
    }
  }

  handleSearch(value) {
    this.setState({
      search: value,
    });
    this.updateFilterData(value);
  }

  updateFilterData(value, nextProps=null) {
    const dataSource = nextProps ? nextProps.dataSource : this.props.dataSource;
    let filterResult = [];

    if (value) {
      filterResult = dataSource.filter(item => {
        for (let key in item) {
          if (typeof item[key] === 'string' && item[key].indexOf(value) > -1) {
            return true;
          }
        }
        return false;
      });
    }
    this.setState({
      filterData: filterResult,
    });
  }

  getDataSource() {
    const { isSearched, dataSource } = this.props;

    if (isSearched) {
      if (this.state.search || this.state.filterData.length) {
        return this.state.filterData;
      } else {
        return dataSource;
      }
    } else {
      return dataSource;
    }
  }

  render() {
    const props = this.props;
    let classes = props.prefixCls;

    if (props.className) {
      classes += props.className;
    }

    return (
      <div className={classes}>
        {(props.isToolbarShowed)
          ? <TableToolbar
              isSearched={props.isSearched}
              searchCol={props.searchCol}
              size={props.size}
              searchPlaceholder={props.searchPlaceholder}
              elements={props.elements}
              onSearch={this.handleSearch}
            />
          : null
        }
        <Table
          rowKey={props.rowKey}
          dataSource={this.getDataSource()}
          columns={props.columns}
          rowSelection={props.rowSelection}
          pagination={props.pagination}
          size={props.size}
          loading={props.loading}
          bordered={props.bordered}
          expandedRowRender={props.expandedRowRender}
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
  isToolbarShowed: false,
  isSearched: false,
  searchPlaceholder: 'search',
  columns: [],
  rowSelection: null,
  size: 'default',
  loading: false,
  bordered: false,
  onChange() {},
  onRowClick() {},
};

TablePlus.propTypes = {
  prefixCls: PropTypes.string,
  className: PropTypes.string,
  isToolbarShowed: PropTypes.bool,
  rowKey: PropTypes.oneOfType([PropTypes.string, PropTypes.func]),
  dataSource: PropTypes.array,
  columns: PropTypes.array,
  rowSelection: PropTypes.object,
  pagination: PropTypes.object,
  size: PropTypes.string,
  loading: PropTypes.bool,
  bordered: PropTypes.bool,
  scroll: PropTypes.object,
  onChange: PropTypes.func,
  onRowClick: PropTypes.func,
  isSearched: PropTypes.bool,
  searchCol: PropTypes.object,
  searchPlaceholder: PropTypes.string,
  elements: PropTypes.array,
  expandedRowRender: PropTypes.func,
};

export default TablePlus;
