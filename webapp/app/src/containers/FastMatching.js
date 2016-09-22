'use strict';
import React, { Component } from 'react';

import Header from '../components/common/Header';
import FilterBox from '../components/fastmatching/FilterBox';
import SearchResultBox from '../components/common/searchresult/SearchResultBox';

import './fastmatching.less';

export default class FastMatching extends Component {

  render() {
    return (
      <div>
        <Header />
        <FilterBox />
        <SearchResultBox />
      </div>
    );
  }
}