'use strict';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import Immutable from 'immutable';
import 'whatwg-fetch';

import Header from '../components/common/Header';
import FilterBox from '../components/fastmatching/FilterBox';
import SearchResultBox from '../components/common/searchresult/SearchResultBox';
import SideBar from '../components/fastmatching/SideBar';

import checkObjectExist from '../utils/check_object_exist';
import './fastmatching.less';

export default class FastMatching extends Component {

  constructor() {
    super();
    this.state = {
      id: '',
      classify: [],
      searchResultDataSource: [],
      pages: 0,
      total: 0,
      spinning: true,
      visible: false,
      postData: {},
      selection: Immutable.List(Immutable.Map()),
    };

    this.loadClassifyData = this.loadClassifyData.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.handleToggleSelection = this.handleToggleSelection.bind(this);
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

  handleSearch(value) {
    const filterData = {};
    for (let key in value) {
      if (key !== 'uses') {
        filterData[key] = value[key];
      }
    }
    const postData = {
      id: '5b8fcdb00d0b11e6bb746c3be51cefca',
      uses: value.uses,
      filterdict: filterData,
    };

    this.setState({
      postData: postData,
      visible: true,
      spinning: true,
    });

    fetch(`/api/mining/lsibyjdid`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    })
    .then(response => response.json())
    .then((json) => {
      this.setState({
          spinning: false,
          searchResultDataSource: json.data.datas,
          pages: json.data.pages,
          total: json.data.totals,
      });
    })
  }

  handleSwitchPage(page) {
    this.setState({
      spinning: true,
      searchResultDataSource: [],
    });
    fetch(`/api/mining/lsibyjdid`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(Object.assign(this.state.postData, { page: page })),
    })
    .then(response => response.json())
    .then((json) => {
      this.setState({
        spinning: false,
        searchResultDataSource: json.data.datas,
      });
    })
  }

  handleToggleSelection(obj) {
    const index = this.state.selection.findIndex(v => {
      return v.get('id') === obj.id 
    });
    if (index > -1) {
      this.setState(({ selection }) => ({
        selection: selection.delete(index)
      }));
    } else {
      this.setState(({ selection }) => ({
        selection: selection.update(sel => {
          return sel.push(Immutable.fromJS(obj))
        })
      }));
    }
  }

  componentDidMount() {
    const url = window.location.href.split('/');

    this.setState({
      id: url[url.length - 1],
    });
    this.loadClassifyData();
  }

  render() {
    return (
      <div>
        <Header />
        <FilterBox
          classify={this.state.classify}
          visible={this.state.visible}
          total={this.state.total}
          onSearch={this.handleSearch}
        />
        <SearchResultBox
          visible={this.state.visible}
          total={this.state.total}
          spinning={this.state.spinning}
          dataSource={this.state.searchResultDataSource}
          selection={this.state.selection}
          onSwitchPage={this.handleSwitchPage}
          onToggleSelection={this.handleToggleSelection}
        />
        <SideBar
          visible={this.state.visible}
          postData={this.state.postData}
          selection={this.state.selection}
          dataSource={this.state.searchResultDataSource}
          onToggleSelection={this.handleToggleSelection}
        />
      </div>
    );
  }
}