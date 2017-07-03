'use strict';
import moment from 'moment';
import React, { Component } from 'react';

import { FilterCard } from 'components/filter-card';
import SearchResultBox from 'components/search-result-box';
import SiderBar from 'components/sider-bar';

import {
  getLSIAllSIMS,
  getIndustry
} from 'request/classify';
import { getFastMatching } from 'request/fastmatching';

import { API } from 'API';

import findIndex from 'lodash/findIndex';

class FastMatching extends Component {
  constructor() {
    super();
    this.state = {
      current: 1,
      id: '',
      postAPI: '',
      classify: [],
      industry: {},
      dataSource: [],
      selection: [],
      visible: false,
      spinning: false,
      siderbarVisible: false,
      siderbarClosable: false,
      textarea: false
    };
    this.handleSearch = this.handleSearch.bind(this);
    this.handleToggleSelection = this.handleToggleSelection.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.getLSIAllSIMSDataSource = this.getLSIAllSIMSDataSource.bind(this);
    this.getIndustryDataSource = this.getIndustryDataSource.bind(this);
    this.getResultDataSource = this.getResultDataSource.bind(this);
  }

  componentDidMount() {
    const { classify } = this.state,
          { location } = this.props;
    let postAPI;

    this.getIndustryDataSource();
    var promise = new Promise((resolve, reject) => {
      this.getLSIAllSIMSDataSource(resolve);
    });

    const date = new Date();
    const defFilterData = {date: [moment(date).add(-180, 'days').format('YYYY-MM-DD'),
                                  moment(date).format('YYYY-MM-DD')]};
    
    if (location.query.jd_id) {
      postAPI = API.LSI_BY_JD_ID_API;

      this.setState({
        id: location.query.jd_id,
        postAPI: postAPI,
        siderbarVisible: true
      });


      promise.then((data) => {
        this.getResultDataSource(postAPI, {
          id: location.query.jd_id,
          uses: data,
          filterdict: defFilterData,
        });
      });
    } else if (location.query.cv_id) {
      postAPI = API.LSI_BY_CV_ID_API;

      this.setState({
        id: location.query.cv_id,
        postAPI: postAPI,
        siderbarClosable: true
      });
      promise.then((data) => {
        this.getResultDataSource(postAPI, {
          id: location.query.cv_id,
          uses: data,
          filterdict: defFilterData,
        });
      });
    } else {
      promise.then((data) => {
        this.setState({
          textarea: true,
          postData: Object.assign({}, {filterdict: defFilterData}),
          postAPI: API.LSI_BY_DOC_API
        });
      });
    }
  }

  /**
   * FilterCard 搜索按钮点击事件
   * 
   * @param {object} fieldValue 表单值对象集合
   * 
   * @memberOf FastMatching
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
    } else {
      postData = {
        id: id,
        uses: fieldValue.uses,
        filterdict: filterData
      };
    }

    this.setState({
      current: 1,
      postData: Object.assign({}, postData, { page: 1 }),
      visible: true,
      spinning: true,
      siderbarVisible: true
    });

    getFastMatching(postAPI, postData, json => {
      this.setState({
        spinning: false,
        dataSource: json.data.datas,
        pages: json.data.pages,
        total: json.data.totals,
      });
    });
  }

  /**
   * Fastmatching结果条目checkbox与右边侧边栏selection box条目的联动功能事件
   * 
   * @param {object} item 当前点击的item对象
   * 
   * @memberOf FastMatching
   */
  handleToggleSelection(item) {
    let selection = this.state.selection;
    const index = findIndex(selection, (obj) => {
      return obj.id === item.id;
    });

    if (index > -1) {
      selection.splice(index, 1);
    } else {
      selection.push(item);
    }
    this.setState({ selection });
  }

  /**
   * 底部翻页按钮功能
   * 
   * @param {number} page 
   * 
   * @memberOf FastMatching
   */
  handleSwitchPage(page) {
    const { postAPI, postData } = this.state;

    this.setState({
      current: page,
      spinning: true,
      dataSource: []
    });

    getFastMatching(postAPI, Object.assign({}, postData, { page: page }), json => {
      if (json.code === 200) {
        this.setState({
          spinning: false,
          dataSource: json.data.datas
        });
      }
    });
  }

  getLSIAllSIMSDataSource(resolve) {
    getLSIAllSIMS(json => {
      if (json.code === 200) {
        this.setState({
          classify: json.data
        });
        resolve(json.data);
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

  getResultDataSource(api, postData) {
    this.setState({
      visible: true,
      spinning: true,
      postData: postData,
    });

    getFastMatching(api, postData, json => {
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
      classify,
      industry,
      postData,
      visible,
      spinning,
      current,
      total,
      dataSource,
      selection,
      siderbarClosable,
      siderbarVisible
    } = this.state;

    return (
      <div className="cs-fast-matching">
        <FilterCard
          textarea={textarea}
          classify={classify}
          industry={industry}
          postData={postData}
          visible={visible}
          total={total}
          onSearch={this.handleSearch}
        />
        <SearchResultBox
          type="match"
          visible={visible}
          spinning={spinning}
          current={current}
          total={total}
          dataSource={dataSource}
          selection={selection}
          educationExperienceText="教育经历"
          workExperienceText="工作经历"
          foldText="展开"
          unfoldText="收起"
          onSwitchPage={this.handleSwitchPage}
          onToggleSelection={this.handleToggleSelection}
        />
        <SiderBar
          closable={siderbarClosable}
          visible={siderbarVisible}
          postData={postData}
          selection={selection}
          dataSource={dataSource}
          onToggleSelection={this.handleToggleSelection}
        />
      </div>
    );
  }
}

export default FastMatching;
