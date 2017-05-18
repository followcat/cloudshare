'use strict';
import React, { Component } from 'react';
import { Tag, Rate, Icon } from 'antd';

import { FilterCard, SearchResultBox } from 'components/analysis-doc';

import Charts from 'components/analysis-doc/Charts';
import ColorGrad from 'utils/color-grad';
import { getRadarOption } from 'utils/chart_option';
import { getDocMining, getDocCVValuable } from 'request/docmining';

import { API } from 'API';
import classNames from 'classnames';

class CVDocMining extends Component {
  constructor() {
    super();
    var option = {
      title: { text: '准备分析' },
      tooltip: {},
      legend: { data: [] },
      radar: { indicator: [] },
      series: [{
          name: '',
          type: 'radar',
          data : []}]
    };
    this.state = {
      current: 1,
      id: '',
      postAPI: '',
      cvpostAPI: '',
      dataSource: [],
      option: option,
      rank:0,
      rate:0,
      stars:0,
      visible: false,
      spinning: false,
      textarea: false,
      cvtextarea: false,
      anonymized: false,
      chartVisible: false,
      addedChartResult: [],
    };
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.getResultDataSource = this.getResultDataSource.bind(this);
  }

  componentDidMount() {
    const { location } = this.props;
    let postAPI;

    this.setState({
      cvtextarea: true,
      postAPI: API.ANALYSIS_BY_DOC_API,
      cvpostAPI: API.MINING_CV_VALUABLE_API
    });
  }

  /**
   * FilterCard 搜索按钮点击事件
   * 
   * @param {object} fieldValue 表单值对象集合
   * 
   * @memberOf CVDocMining
   */
  handleSearch(fieldValue) {
    const { id, postAPI, cvpostAPI, chartVisible, addedChartResult,
            rate, rank, stars } = this.state;
    let filterData = {},
        postData = {};
    var option = {
      title: { text: '正在分析' },
      tooltip: {},
      legend: { data: [] },
      radar: { indicator: [] },
      series: [{
          name: '',
          type: 'radar',
          data : []}]
    };

    for (let key in fieldValue) {
      if (key !== 'uses' && key !== 'doc' && key !== 'cv') {
        if (fieldValue[key] instanceof Array) {
          filterData[key] = fieldValue[key];
        } else {
          filterData[key] = fieldValue[key] ? fieldValue[key].split(' ') : [];
        }
      }
    }

    if (typeof fieldValue.doc !== 'undefined' && typeof fieldValue.cv !== 'undefined') {
      postData = {
        cv: fieldValue.cv,
        doc: fieldValue.doc,
        uses: fieldValue.uses,
        filterdict: filterData
      };

      this.setState({
        current: 1,
        postData: Object.assign({}, postData, { page: 1 }),
        visible: true,
        spinning: true,
        option: option,
      });

      getDocMining(postAPI, postData, json => {
        this.setState({
          spinning: false,
          chartVisible: true,
          dataSource: json.data.datas,
          pages: json.data.pages,
          total: json.data.totals,
        });
        getDocCVValuable(cvpostAPI, postData, json => {
          if (json.code === 200) {
            this.setState({
              rate: json.rate,
              rank: json.rank,
              stars: json.stars,
              addedChartResult: [json.data.result],
              option: getRadarOption(json.data.max, json.data.result, this.state.anonymized),
            });
          }
        });
      });

    }
  }

  /**
   * 底部翻页按钮功能
   * 
   * @param {number} page 
   * 
   * @memberOf CVDocMining
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
      option,
      textarea,
      cvtextarea,
      postData,
      visible,
      spinning,
      current,
      total,
      rank,
      rate,
      stars,
      dataSource,
      chartVisible,
      addedChartResult,
    } = this.state;

    const { prefixCls } = this.props;
    const classSet = classNames({
      [`${prefixCls}`]: true,
      'showed': chartVisible === true,
      'hidden': chartVisible === false,
    });
    const colorGrad = new ColorGrad();
    const linkColor = { color: colorGrad.gradient()[parseInt(rate*100)],
                        fontWeight: 600 };

    return (
      <div className="cs-fast-matching">
        <FilterCard
          textarea={false}
          textareaWithCV={cvtextarea}
          onSearch={this.handleSearch}
        />
        <div className={classSet}>
          <div style={{ fontSize: 16, textAlign: 'center', marginBottom: 10 }}>
            <font>评分为</font><font style={linkColor}>{rate}</font>.
            { (stars
                ?
                  <font>恭喜!你名列前矛,你在我们的人才库中排名
                  <Tag color="#2db7f5">{rank}</Tag>
                  被系统判断为
                  <Rate disabled={true}
                        value={stars}
                  />星简历</font>
                : <font>评分较低建议修改简历</font>
              )}
          </div>
          <Charts
            option={option}
            style={{ width: 900, height: 380, margin: '0 auto' }} />
        </div>
        <SearchResultBox
          type="match"
          visible={visible}
          spinning={spinning}
          current={current}
          total={total}
          postData={postData}
          dataSource={dataSource}
          addedChartResult={addedChartResult}
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

CVDocMining.defaultProps = {
  prefixCls: 'cvdoc-result'
};

export default CVDocMining;
