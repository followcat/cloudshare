'use strict';
import React, { Component } from 'react';

import { hashHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import DatabaseInfo from './DatabaseInfo';

class Search extends Component {
  constructor() {
    super();
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleSearch(value) {
    hashHistory.push(`/result?search_text=${value}`);
  }

  render() {
    return (
      <div className="cs-layout-search">
        <KeywordSearch
          btnText="搜索"
          horizontal
          onSearch={this.handleSearch}
        />
        <DatabaseInfo />
      </div>
    );
  }
}

export default Search;
