'use strict';
import React, { Component, PropTypes } from 'react';
import { browserHistory } from 'react-router';

import KeywordSearch from 'components/keyword-search';
import SearchResultBox from 'components/jd-search-result-box';
import ResultInfo from './ResultInfo';

import { jdMatching } from 'request/matching';
import { getIndustry } from 'request/classify';

class SearchResult extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchText: props.location.query.search_text,
      dataSource: [],
      pages: 0,
      current: 1,
      totals: 1,
      spinning: false,
      filterValue: {},
      industry: {}
    };
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.handleFilter = this.handleFilter.bind(this);
    this.getIndustryDataSource = this.getIndustryDataSource.bind(this);
    this.loadResultDataSource = this.loadResultDataSource.bind(this);
  }

  componentDidMount() {
    this.loadResultDataSource(this.state.searchText);
    this.getIndustryDataSource();
  }

  handleSearch(value) {
    browserHistory.push(`/jobsearch/result?search_text=${value}`);

    this.setState({
      searchText: value,
      page: 0,
      current: 1,
      totals: 1,
    });

    this.loadResultDataSource(value);
  }

  handleSwitchPage(page) {
    const { filterValue } = this.state;

    this.setState({
      current: page,
      spinning: true,
      dataSource: []
    });

    jdMatching({
      'doc': this.state.searchText,
      'page': page-1,
      'numbers':20
    }, json => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          dataSource: json.data,
          totals: json.lenght
        });
      }
    });
  }

  handleFilter(fieldValue) {
    const { searchText } = this.state;
    let filterData = {};
  
    this.setState({
      spinning: true,
      filterValue: fieldValue
    });

    for (let key in fieldValue) {
      if (fieldValue[key] instanceof Array) {
        filterData[key] = fieldValue[key];
      } else {
        filterData[key] = fieldValue[key] ? fieldValue[key].split(' ') : [];
      }
    }

    jdMatching({
      'doc': searchText,
      'page': 0,
      'numbers': 20
    }, (json) => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          pages: json.data.pages,
          dataSource: json.data,
          totals: json.lenght
        });
      }
    });
  }

  getIndustryDataSource() {
    getIndustry(json => {
      if (json.code === 200) {
        this.setState({
          industry: json.data
        });
      }
    });
  }

  loadResultDataSource(searchText) {
    this.setState({
      spinning: true
    });

    jdMatching({
      doc: searchText,
      page: 0,
      numbers: 20
    }, json => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
          spinning: false,
          totals: json.lenght
        });
      }
    });
  }

  render() {
    const { prefixCls, location } = this.props,
          { totals,
            searchText,
            current,
            spinning,
            dataSource,
            industry
          } = this.state;

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
            industry={industry}
            onFilter={this.handleFilter}
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
