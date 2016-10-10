'use strict';
import React, { Component } from 'react';

import Header from '../components/common/Header';
import KeywordSearch from '../components/search/KeywordSearch';
import DataBaseBox from '../components/common/DataBaseBox';

import './search.less';

export default class Search extends Component {
  render() {
    return (
      <div id="viewport">
        <Header />
        <div className="cs-layout-container">
          <KeywordSearch />
          <DataBaseBox />
        </div>
      </div>
    );
  }
}