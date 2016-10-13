'use strict';
import React, { Component } from 'react';

import Header from '../components/common/Header';
import ResultInfo from '../components/search/ResultInfo';
import SearchResultBox from '../components/common/searchresult/SearchResultBox';

import queryString from '../utils/query_string';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';

import './searchresult.less';

export default class SearchResult extends Component {

  constructor() {
    super();
    this.state = {
      keyword: '',
      pages: 0,
      total: 0,
      spinning: false,
      visible: false,
      data: [],
    };
    this.loadSearchResult = this.loadSearchResult.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.handleOnSearch = this.handleOnSearch.bind(this);
  }

  loadSearchResult(searchText) {
    this.setState({
      spinning: true,
    });
    fetch(`/api/searchbytext`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        // 'search_text': searchText,
        'search_text': 'software engineer',
      })
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          pages: json.data.pages,
          total: json.data.totals,
          data: json.data.datas,
          spinning: false,
        });
      }
    })
  }

  componentDidMount() {
    const url = window.location.href,
          params = queryString(url);
    this.setState({
      keyword: params.search_text,
    });
    this.loadSearchResult(params.search_text);
  }

  handleSwitchPage(page) {
    this.setState({
      spinning: true,
      data: [],
    });

    fetch(`/api/searchbytext`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        'search_text': this.state.keyword,
        'page': page,
      })
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          data: json.data.datas,
        });
      }
    })
  }

  handleOnSearch(searchText) {
    this.setState({
      keyword: searchText,
      pages: 0,
      total: 0,
      spinning: true,
      data: [],
    });

    fetch(`/api/searchbytext`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'search_text': searchText,
      })
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          pages: json.data.pages,
          total: json.data.totals,
          data: json.data.datas,
        });
      }
    })
  }

  render() {
    return (
      <div>
        <Header
          search={this.state.keyword}
          onSearch={this.handleOnSearch}
        />
        <div style={{ marginTop: 24 }}>
          <ResultInfo 
            total={this.state.total}
            keyword={this.state.keyword}
            dataSource={this.state.data}
          />
          <SearchResultBox
            visible={true}
            total={this.state.total}
            spinning={this.state.spinning}
            dataSource={this.state.data}
            onSwitchPage={this.handleSwitchPage}
          />
        </div>
      </div>
    );
  }
}