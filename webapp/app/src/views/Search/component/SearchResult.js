'use strict';
import React, { Component, PropTypes } from 'react';
import { browserHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import SearchResultBox from 'components/search-result-box';
import ResultInfo from './ResultInfo';

import { getResultData } from 'request/search';

class SearchResult extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchText: props.location.query.search_text,
      dataSource: [],
      pages: 0,
      current: 1,
      totals: 0,
      spinning: false
    };
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.loadResultDataSource = this.loadResultDataSource.bind(this);
  }

  componentDidMount() {
    this.loadResultDataSource(this.state.searchText);
  }

  handleSearch(value) {
    browserHistory.push(`/result?search_text=${value}`);

    this.setState({
      searchText: value,
      pages: 0,
      current: 1,
      totals: 0,
    });

    this.loadResultDataSource(value);
  }

  handleSwitchPage(page) {
    this.setState({
      current: page,
      spinning: true,
      dataSource: [],
    });

    getResultData({
      'search_text': this.state.searchText,
      'page': page
    }, json => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          dataSource: json.data.datas
        });
      }
    });
  }

  loadResultDataSource(searchText) {
    this.setState({
      spinning: true
    });

    getResultData({
      search_text: searchText
    }, json => {
      if (json.code === 200) {
        this.setState({
          pages: json.data.pages,
          totals: json.data.totals,
          dataSource: json.data.datas,
          spinning: false
        });
      }
    });
  }

  render() {
    const { prefixCls, location } = this.props,
          { totals, searchText, current, spinning, dataSource } = this.state;

    return (
      <div className={prefixCls}>
        <div className={`${prefixCls}-top`}>
          <KeywordSearch
            defaultValue={location.query.search_text}
            btnText="搜索"
            onSearch={this.handleSearch}
            inline
          />
        </div>
        <div className={`${prefixCls}-container`}>
          <ResultInfo
            total={totals}
            keyword={searchText}
            dataSource={dataSource}
          />
          <SearchResultBox
            visible={true}
            current={current}
            total={totals}
            spinning={spinning}
            dataSource={dataSource}
            educationExperienceText="教育经历"
            workExperienceText="工作经历"
            foldText="展开"
            unfoldText="收起"
            onSwitchPage={this.handleSwitchPage}
          />
        </div>
      </div>
    );
  }
}

SearchResult.defaultProps = {
  prefixCls: 'cs-search-result'
};

SearchResult.propTypes = {
  prefixCls: PropTypes.string,
  location: PropTypes.object
};

export default SearchResult;
