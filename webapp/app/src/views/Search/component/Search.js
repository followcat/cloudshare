'use strict';
import React, { Component } from 'react';

import { browserHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import DatabaseInfo from './DatabaseInfo';

class Search extends Component {
  constructor() {
    super();
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleSearch(value) {
    browserHistory.push(`/result?search_text=${value}`);
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
