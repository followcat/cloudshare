'use strict';
import React, { Component } from 'react';

import Immutable from 'immutable';
import 'whatwg-fetch';

import Header from 'components/common/Header';
import FilterBox from 'components/fastmatching/FilterBox';
import SearchResultBox from 'components/common/searchresult/SearchResultBox';
import SideBar from 'components/fastmatching/SideBar';

import StorageUtil from 'utils/storage';
import Generator from 'utils/generator';
import queryString from 'utils/query_string';
import { API } from 'API';

import { getIndustry } from 'request/classify';

import './fastmatching.less';

export default class FastMatching extends Component {

  constructor() {
    super();
    this.state = {
      current: 1,  // 当前页
      id: '',
      classify: [],
      industry: {},
      searchResultDataSource: [],
      pages: 0,
      total: 0,
      spinning: true,
      visible: false,
      siderbarClosable: false,
      siderbarVisible: false,
      textarea: false,
      appendCommentary: false,
      postData: {},
      postAPI: '',
      selection: Immutable.List(Immutable.Map()),
    };

    this.loadClassifyData = this.loadClassifyData.bind(this);
    this.loadIndustry = this.loadIndustry.bind(this);
    this.loadResultData = this.loadResultData.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.handleToggleSelection = this.handleToggleSelection.bind(this);
  }

  /**
   * [初始加载classify列表]
   * @return {[type]} [description]
   */
  loadClassifyData(id = null, postAPI = null, appendCommentary = false) {
    fetch(`/api/classify`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(),
    })
    .then(response => response.json())
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          classify: json.data,
        });
        if (id && postAPI) {
          this.loadResultData(id, postAPI, json.data, appendCommentary);
        }
      }
    })
  }

  loadIndustry() {
    getIndustry(json => {
      if (json.code === 200) {
        this.setState({
          industry: json.data
        });
      }
    });
  }

  /**
   * 初始加载默认的fastmatching结果
   * @param  {[string]} id [JD id]
   * @return {[type]}    [description]
   */
  loadResultData(id, postAPI, classify, appendCommentary) {
    let postData = { id: id, uses: classify, appendcomment: appendCommentary };
    this.setState({
      visible: true,
      spinning: true,
      postData: postData,
    });

    fetch(postAPI, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(postData),
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

  /**
   * Filter表单的过滤功能事件
   * @param  {[object]} value [表单对象数据]
   * @return {[type]}       [description]
   */
  handleSearch(value) {
    let filterData = {},
          postData = {};

    for (let key in value) {
      if (key !== 'uses' && key !== 'doc' && key !== 'appendcomment') {
        filterData[key] = value[key] instanceof Array ? value[key] : value[key] ? value[key].split(' ') : [];
      } else if (key === 'appendcomment') {
        this.setState({
          appendcomment: value[key]
        });
        postData = { appendcomment: value[key] };
      }
    }

    if (value.doc) {
      postData = Object.assign({}, postData, {
        doc: value.doc,
        uses: value.uses,
        filterdict: filterData,
      });
    } else {
      postData = Object.assign({}, postData, {
        id: this.state.id,
        uses: value.uses,
        filterdict: filterData,
      });
    }

    this.setState({
      current: 1,
      postData: Object.assign({}, postData, { page: 1 }),
      visible: true,
      spinning: true,
      siderbarVisible: true,
    });

    fetch(this.state.postAPI, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(postData),
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

  /**
   * 底部翻页按钮功能
   * @param  {[int]} page [页码]
   * @return {[type]}      [description]
   */
  handleSwitchPage(page) {
    this.setState({
      current: page,
      spinning: true,
      searchResultDataSource: [],
    });
    console.log(this.state.postData);
    fetch(this.state.postAPI, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(Object.assign({}, this.state.postData, { page: page })),
    })
    .then(response => response.json())
    .then((json) => {
      this.setState({
        spinning: false,
        searchResultDataSource: json.data.datas,
      });
    })
  }

  /**
   * Fastmatching结果条目checkbox与右边侧边栏selection box条目的联动功能
   * @param  {[object]} obj [当前点击的item对象]
   * @return {[type]}     [description]
   */
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
    const params = queryString(window.location.href),
          jd_id = params.jd_id || null,
          cv_id = params.cv_id || null,
          append_commentary = params.init_append_commentary === 'true' ? true : false;
    let postAPI;

    // this.loadClassifyData();
    this.loadIndustry();

    if (jd_id) {
      postAPI = API.LSI_BY_JD_ID_API;
      this.setState({
        id: jd_id,
        postAPI: postAPI,
        siderbarVisible: true,
        appendCommentary: append_commentary
      });
      this.loadClassifyData(jd_id, postAPI, append_commentary);
    } else if (cv_id) {
      postAPI = API.LSI_BY_CV_ID_API;
      this.setState({
        siderbarClosable: true,
        id: cv_id,
        postAPI: postAPI,
      });
      this.loadClassifyData(cv_id, postAPI);
    } else {
      this.setState({
        textarea: true,
        postAPI: API.LSI_BY_DOC_API,
      });
      this.loadClassifyData();
    }
  }

  render() {
    return (
      <div>
        <Header />
        <FilterBox
          textarea={this.state.textarea}
          classify={this.state.classify}
          industry={this.state.industry}
          visible={this.state.visible}
          appendCommentary={this.state.appendCommentary}
          total={this.state.total}
          onSearch={this.handleSearch}
        />
        <SearchResultBox
          type="match"
          visible={this.state.visible}
          current={this.state.current}
          total={this.state.total}
          spinning={this.state.spinning}
          dataSource={this.state.searchResultDataSource}
          selection={this.state.selection}
          onSwitchPage={this.handleSwitchPage}
          onToggleSelection={this.handleToggleSelection}
        />
        <SideBar
          closable={this.state.siderbarClosable}
          visible={this.state.siderbarVisible}
          postData={this.state.postData}
          selection={this.state.selection}
          dataSource={this.state.searchResultDataSource}
          onToggleSelection={this.handleToggleSelection}
        />
      </div>
    );
  }
}