'use strict';
import React, { Component } from 'react';

import SearchResultHeader from './SearchResultHeader';

import './searchresult.less';

export default class SearchResultBox extends Component {
  render() {
    return (
      <div className="cv-search-result">
        <SearchResultHeader />
      </div>
    );
  }
}