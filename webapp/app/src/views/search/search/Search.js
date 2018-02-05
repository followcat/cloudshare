'use strict';
import React, { Component } from 'react';

import { browserHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import Guide from 'components/guide';
import DatabaseInfo from './DatabaseInfo';

import { introJs } from 'intro.js';

import { Steps, Icon, Tabs } from 'antd';
import websiteText from 'config/website-text';

import StorageUtil from 'utils/storage'

const language = websiteText.zhCN;
const Step = Steps.Step;
const TabPane = Tabs.TabPane;

class Search extends Component {
  constructor() {
    super();
    this.state = {
      ismember: StorageUtil.get('ismember')
    }
    this.handleSearch = this.handleSearch.bind(this);
    this.handleJDSearch = this.handleJDSearch.bind(this);
    this.handleCOSearch = this.handleCOSearch.bind(this);
  }

  handleSearch(value) {
    browserHistory.push({
      pathname: 'search/result',
      query: { search_text: value }
    });
  }

  handleJDSearch(value) {
    browserHistory.push({
      pathname: '/fastmatching',
      query: { match_doc: value }
    });
  }

  handleCOSearch(value) {
    browserHistory.push({
      pathname: '/cosearch/result',
      query: { search_text: value }
    });
  }

  render() {
    return (
      <div className="cs-layout-search">
        <Guide />
        <div className="card-container">
          <div className="cs-search">
            <Tabs type="card">
            {this.state.ismember &&
              <TabPane tab={language.JD_SEARCH} key="1">
                <KeywordSearch
                  btnText={language.JD_SEARCH}
                  horizontal
                  onSearch={this.handleSearch}
                />
              </TabPane>
            }
              <TabPane tab={language.JOBSEARCH} key="2">
                <KeywordSearch
                  btnText={language.JOBSEARCH}
                  defaultText={'输入职位职责进行匹配'}
                  horizontal
                  onSearch={this.handleJDSearch}
                />
              </TabPane>
              <TabPane tab={language.COMPANY_SEARCH} key="3">
                <KeywordSearch
                  btnText={language.COMPANY_SEARCH}
                  defaultText={'输入公司名进行搜索'}
                  horizontal
                  onSearch={this.handleCOSearch}
                />
              </TabPane>
              </Tabs>
          </div>
        </div>
        <DatabaseInfo />
      </div>
    );
  }
}

export default Search;
