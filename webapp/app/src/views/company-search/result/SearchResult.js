'use strict';
import React, { Component, PropTypes } from 'react';
import { browserHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import SearchResultBox from 'components/co-search-result-box';
import ResultInfo from './ResultInfo';

import { Pagination } from 'antd';

import { searchCompany } from 'request/company';

class SearchResult extends Component {
  constructor(props) {
    super(props);
    this.state = {
      startColor: '#00ff0a',
      endColor: '#000000',
      pageSize: 20,
      searchText: props.location.query.search_text,
      dataSource: [],
      pages: 1,
      current: 1,
      totals: 1,
      spinning: false,
      filterValue: {},
      industry: {}
    };
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.loadResultDataSource = this.loadResultDataSource.bind(this);
    this.handleShowSizeChange = this.handleShowSizeChange.bind(this);
    this.handlePaginationChange = this.handlePaginationChange.bind(this);
  }

  componentWillMount() {
    const { searchText, pages, pageSize} = this.state;

    if(searchText) {
      this.loadResultDataSource(searchText,pages,pageSize);
    }
  }

  componentDidMount() {
    // this.loadResultDataSource(this.state.searchText);
  }

  handleShowSizeChange(current, pageSize) {
      this.setState({
        current: current,
        pageSize: pageSize
      },() => this.handleSwitchPage(current));
  }

  handlePaginationChange(current) {
      this.setState({
        current: current
      },() => {this.handleSwitchPage(current)});
  }

  handleSearch(value) {
    const { pages, pageSize } = this.state;
    browserHistory.push(`/cosearch/result?search_text=${value}`);
    this.setState({
      searchText: value,
      pages: 1,
      current: 1,
      totals: 1,
    });
    console.log(value);
    this.loadResultDataSource(value,pages,pageSize);
  }

  handleSwitchPage(page) {
    const { searchText, filterValue, pageSize } = this.state;

    this.setState({
      current: page,
      spinning: true,
      dataSource: []
    });

    this.loadResultDataSource(searchText,page,pageSize);
  }

  loadResultDataSource(searchText,page,size) {
    this.setState({
      spinning: true
    });

    searchCompany({
      param:'q='+searchText+'&page='+page+'&size='+size,
    }, json => {
      if (json.data.length > 0) {
        this.setState({
          dataSource: json.data,
          spinning: false,
          totals: json.total
        });
      }
    });
  }

  render() {
    const { prefixCls, location } = this.props,
          { startColor,
            endColor,
            totals,
            pageSize,
            searchText,
            current,
            spinning,
            dataSource,
            industry
          } = this.state;

    const pagination = {
      current: current,
      total: totals,
      pageSize: pageSize,
      showSizeChanger: true,
      showQuickJumper: true,
      defaultPageSize: 20,
      showTotal: totals => `共 ${totals} 条`,
      onShowSizeChange: this.handleShowSizeChange,
      onChange: this.handlePaginationChange
    };

    return (
      <div className={prefixCls}>
        <div className={`${prefixCls}-top`}>
          <KeywordSearch
            defaultValue={location.query.search_text}
            btnText="公司搜索"
            onSearch={this.handleSearch}
            inline
          />
        </div>
        <div className={`${prefixCls}-container`}>
          <ResultInfo
            total={totals}
            keyword={searchText}
            dataSource={dataSource}
            industry={industry}
            onFilter={this.handleFilter}
          />
          <SearchResultBox
            visible={true}
            current={current}
            total={totals}
            spinning={spinning}
            startColor={startColor}
            endColor={endColor}
            searchText={searchText}
            dataSource={dataSource}
            educationExperienceText="教育经历"
            workExperienceText="工作经历"
            foldText="展开"
            unfoldText="收起"
            onSwitchPage={this.handleSwitchPage}
          />
        </div>
        <div className="cs-card-inner-pagination">
          <Pagination {...pagination}/>
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
