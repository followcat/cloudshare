'use strict';
import React, { Component, PropTypes } from 'react';

import { Spin } from 'antd';

import SearchResultHeader from './SearchResultHeader';
import SearchResultItem from './SearchResultItem';
import SearchResultPagination from './SearchResultPagination';

import './searchresult.less';

export default class SearchResultBox extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="cs-search-result">
        <Spin spinning={this.props.spinning}>
          <SearchResultHeader />
          {this.props.dataSource.map((item, index) => {
            return <SearchResultItem key={index} {...item} />
          })}
        </Spin>
        <SearchResultPagination />
      </div>
    );
  }
}

SearchResultBox.propTypes = {
  dataSource: PropTypes.array,
};