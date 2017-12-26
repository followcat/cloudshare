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

  UploadClick(){
    browserHistory.push({
      pathname: 'uploader?guide=true',
      query: { search_text: true }
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
              </Tabs>
          </div>
        </div>
        <DatabaseInfo />
      </div>
    );
  }
}

export default Search;
