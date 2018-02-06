'use strict';
import React, { Component } from 'react';

import { browserHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import Guide from 'components/guide';
import DatabaseInfo from './DatabaseInfo';

import { introJs } from 'intro.js';

import { Steps, Icon } from 'antd';
const Step = Steps.Step;

class Search extends Component {
  constructor() {
    super();
    this.handleSearch = this.handleSearch.bind(this);
  }

  handleSearch(value) {
    browserHistory.push({
      pathname: 'cosearch/result',
      query: { search_text: value }
    });
  }

  render() {
    return (
      <div className="cs-layout-search">
        <Guide />
        <div className="cs-cosearch">
          <KeywordSearch
            btnText="公司搜索"
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
