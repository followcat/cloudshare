'use strict';
import React, { Component } from 'react';

import Header from '../components/common/Header';
import FilterBox from '../components/fastmatching/FilterBox';
import SearchResultBox from '../components/common/searchresult/SearchResultBox';

import './fastmatching.less';

export default class FastMatching extends Component {

  constructor() {
    super();
    this.state = {
      classify: [],
      searchResultDataSource: [],
      pages: 0,
      total: 0,
      spinning: true,
    };

    this.loadSearchResultData = this.loadSearchResultData.bind(this);
  }

  loadClassifyData() {
    fetch(`/api/classify`, {
      method: 'GET',
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          classify: json.data,
        });
      }
    })
  }

  loadSearchResultData() {
    this.setState({
      spinning: true,
    });

    fetch(`/api/mining/lsibyjdid/e761265657c311e6b4544ccc6a30cd76`, {
      method: 'GET',
      credentials: 'include',
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          searchResultDataSource: json.data.datas,
          pages: json.data.pages,
          total: json.data.totals,
          spinning: false,
        });
      }
    });
  }

  componentDidMount() {
    this.loadClassifyData();
    this.loadSearchResultData();
  }

  render() {
    return (
      <div>
        <Header />
        <FilterBox
          classify={this.state.classify}
          total={this.state.total}
        />
        <SearchResultBox
          spinning={this.state.spinning}
          dataSource={this.state.searchResultDataSource}
        />
      </div>
    );
  }
}