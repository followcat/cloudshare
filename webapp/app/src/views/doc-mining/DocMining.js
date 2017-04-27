'use strict';
import React, { Component } from 'react';

import { FilterCard, SearchResultBox } from 'components/analysis-doc';

import { getDocMining } from 'request/docmining';

import { API } from 'API';

class DocMining extends Component {
  constructor() {
    super();
    this.state = {
      current: 1,
      id: '',
      postAPI: '',
      dataSource: [],
      visible: false,
      spinning: false,
      textarea: false
    };
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.getResultDataSource = this.getResultDataSource.bind(this);
  }

  componentDidMount() {
    const { location } = this.props;
    let postAPI;

    this.setState({
      textarea: true,
      postAPI: API.ANALYSIS_BY_DOC_API
    });
  }

  /**
   * FilterCard 搜索按钮点击事件
   * 
   * @param {object} fieldValue 表单值对象集合
   * 
   * @memberOf DocMining
   */
  handleSearch(fieldValue) {
    const { id, postAPI } = this.state;
    let filterData = {},
        postData = {};

    for (let key in fieldValue) {
      if (key !== 'uses' && key !== 'doc') {
        if (fieldValue[key] instanceof Array) {
          filterData[key] = fieldValue[key];
        } else {
          filterData[key] = fieldValue[key] ? fieldValue[key].split(' ') : [];
        }
      }
    }

    if (typeof fieldValue.doc !== 'undefined') {
      postData = {
        doc: fieldValue.doc,
        uses: fieldValue.uses,
        filterdict: filterData
      };

      this.setState({
        current: 1,
        postData: Object.assign({}, postData, { page: 1 }),
        visible: true,
        spinning: true,
      });

      getDocMining(postAPI, postData, json => {
        this.setState({
          spinning: false,
          dataSource: json.data.datas,
          pages: json.data.pages,
          total: json.data.totals,
        });
      });
    }
  }

  /**
   * 底部翻页按钮功能
   * 
   * @param {number} page 
   * 
   * @memberOf DocMining
   */
  handleSwitchPage(page) {
    const { postAPI, postData } = this.state;

    this.setState({
      current: page,
      spinning: true,
      dataSource: []
    });

    getDocMining(postAPI, Object.assign({}, postData, { page: page }), json => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          dataSource: json.data.datas
        });
      }
    });
  }

  getResultDataSource(api, postData) {
    this.setState({
      visible: true,
      spinning: true,
      postData: postData,
    });

    getDocMining(api, postData, json => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          dataSource: json.data.datas,
          pages: json.data.pages,
          total: json.data.totals
        });
      }
    });
  }

  render() {
    const {
      textarea,
      postData,
      visible,
      spinning,
      current,
      total,
      dataSource,
    } = this.state;

    return (
      <div className="cs-fast-matching">
        <FilterCard
          textarea={textarea}
          onSearch={this.handleSearch}
        />
        <SearchResultBox
          type="match"
          visible={visible}
          spinning={spinning}
          current={current}
          total={total}
          postData={postData}
          dataSource={dataSource}
          educationExperienceText="教育经历"
          workExperienceText="工作经历"
          foldText="展开"
          unfoldText="收起"
          onSwitchPage={this.handleSwitchPage}
        />
      </div>
    );
  }
}

export default DocMining;
