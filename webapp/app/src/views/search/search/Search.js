'use strict';
import React, { Component } from 'react';

import { browserHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import Layout from 'views/common/Layout';
import DatabaseInfo from './DatabaseInfo';

class Search extends Component {
  constructor() {
    super();
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleSearch(value) {
    browserHistory.push({
      pathname: 'search/result',
      query: { search_text: value }
    });
  }

  render() {
    return (
      <div className="cs-layout-search">
        <div className="cs-search">
          <KeywordSearch
            btnText="搜索"
            horizontal
            onSearch={this.handleSearch}
          />
        </div>
        <DatabaseInfo />
      </div>
    );
  }
}

export default Search;
