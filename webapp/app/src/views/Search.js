'use strict';
import React, { Component } from 'react';

import Header from 'components/common/Header';
import KeywordSearch from 'components/search/KeywordSearch';
import DataBaseBox from 'components/common/DataBaseBox';

import './search.less';

export default class Search extends Component {

  constructor() {
    super();

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(searchText) {
    const path = `/search/result?search_text=${searchText}`;
    window.location.href = path;
  }

  render() {
    return (
      <div id="viewport" className="pd-top">
        <Header fixed={true} />
        <div className="cs-layout-container">
          <KeywordSearch onSubmit={this.handleSubmit}/>
          <DataBaseBox />
        </div>
      </div>
    );
  }
}