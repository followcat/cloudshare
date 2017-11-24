'use strict';
import moment from 'moment';
import React, { Component } from 'react';

import { FilterCard } from 'components/filter-card';
import SearchResultBox from 'components/search-result-box';
import SiderBar from 'components/sider-bar';
import Guide from 'components/guide';

import { introJs } from 'intro.js';

import {
  getLSIAllSIMS,
  getIndustry
} from 'request/classify';
import { getFastMatching } from 'request/fastmatching';

import { API } from 'API';

import findIndex from 'lodash/findIndex';

class FastMatching extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: 1,
      id: '',
      postAPI: '',
      searchText: props.location.query.search_text,
      classify: [],
      projects: [],
      industry: {},
      dataSource: [],
      selection: [],
      guide: false,
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

  componentWillMount () {
    const { location } = this.props;
    if(location.query.guide) {
      this.setState({
        guide: true,
        siderbarVisible: true,
        visible: true,
      })
    }
  }

  componentDidMount() {
    const { classify, projects } = this.state,
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

    if(this.state.searchText){
      promise.then((uses) => {
        this.setState({
          postData: Object.assign({uses}, {filterdict: {}},{doc:this.state.searchText}),
          postAPI: API.LSI_BY_DOC_API
        },() => {
          this.getResultDataSource(this.state.postAPI,this.state.postData);
        });
      });
    }

    if(this.state.guide) {
      introJs().setOptions({
        'skipLabel': '退出', 
        'prevLabel':'上一步', 
        'nextLabel':'下一步',
        'doneLabel': '完成',
        'scrollToElement': false,
        steps: [                    
                    {
                        //第一步引导
                        element: '.ant-card-body',
                        intro: '职位描述较关键词匹配更精确，可以选择多种筛选条件。'+
                        '<a href="/pm/jobdescription" target="_blank">推荐使用会员服务-已开放职位的匹配!</a>',
                        position: 'right'
                    },
                    {
                        element: '.cs-search-result',
                        intro: '匹配结果展示，可以勾选多个结果后对比',
                        position: 'bottom'
                    },
                    {
                        //这个属性类似于jquery的选择器， 可以通过jquery选择器的方式来选择你需要选中的对象进行指引
                        element: '.anticon-caret-left',
                        //这里是每个引导框具体的文字内容，中间可以编写HTML代码
                        intro: '勾选后点击侧边栏，选择雷达图或者分析，进行可视化分析数据。',
                        //这里可以规定引导框相对于选中对象出现的位置 top,bottom,left,right
                        position: 'top'
                    },
                ]

      }).start()
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
          classify: json.classify,
          projects: json.projects
        });
        resolve(json.projects.concat(json.classify));
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
      projects,
      industry,
      postData,
      visible,
      spinning,
      current,
      total,
      searchText,
      dataSource,
      selection,
      siderbarClosable,
      siderbarVisible
    } = this.state;
    return (
      <div className="cs-fast-matching">
        <Guide />
        <FilterCard
          textarea={textarea}
          searchText={searchText}
          classify={classify}
          projects={projects}
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
