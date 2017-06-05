'use strict';
import React, { Component } from 'react';
import { Tag, Rate, Icon, Row, Col, message } from 'antd';

import ShowCard from 'components/show-card';
import Charts from 'components/analysis-doc/Charts';
import DraggerUpload from 'components/dragger-upload';
import { FilterCard, SearchResultBox } from 'components/analysis-doc';

import ColorGrad from 'utils/color-grad';
import { getRadarOption } from 'utils/chart_option';
import { getDocMining, getDocCVValuable } from 'request/docmining';

import { API } from 'API';
import classNames from 'classnames';

import remove from 'lodash/remove';
import findIndex from 'lodash/findIndex';

class CVsDocMining extends Component {
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
      textarea: true,
      anonymized: false,
      chartVisible: false,
      addedChartResult: [],
      fileList: [],
      failedList: [],
      confirmList: [],
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.handleSearch = this.handleSearch.bind(this);
    this.handleSwitchPage = this.handleSwitchPage.bind(this);
    this.getResultDataSource = this.getResultDataSource.bind(this);
  }

  componentDidMount() {
    const { location } = this.props;
    let postAPI;

    this.setState({
      postAPI: API.ANALYSIS_BY_DOC_API,
      cvpostAPI: API.MINING_CV_VALUABLE_API
    });
  }

  handleChange(info) {
    let fileList = info.fileList,
        { confirmList, failedList } = this.state;
    fileList = fileList.map(file => {
      if (file.response && file.status === 'done' && !file.completed) {
        file.completed = true;  // 标记已经上传文件, 避免重复请求preview API
        if (file.response.code === 200) {  // 上传成功后,请求预览数据
          file.status = 'done';
          confirmList.push(file.response.data[0]);
        } else {  // 上传失败
          message.error(`${file.name} 上传失败!`, 3);
          file.status = 'error';
          failedList.push({
            id: '',
            status: 'error',
            message: '超时! 系统无法解析该文件',
            filename: file.name,
            uid: file.uid,
          });
        }
      }
      return file;
    });
    var showedList = fileList.filter(function (value) {
              return (value.status === 'uploading' || value.status === 'error');
             })
    this.setState({
      confirmList: confirmList,
      failedList: failedList,
      total: confirmList.length,
      fileList: showedList,
    });
  }

  handleRemove(file) {
    let {
      confirmList,
      failedList,
    } = this.state,
      index = null;

    const removeItem = (key, value, array) => {
      return remove(array, (item) => {
        return item[key] !== value;
      });
    };

    index = findIndex(confirmList, item => item.uid === file.uid);
    confirmList = removeItem('filename', file.filename, confirmList);
    confirmList = removeItem('filename', file.filename, failedList);

    this.setState({
      confirmList: confirmList,
    });
    return file;
  }

  handleSearch(fieldValue) {
    const { id, postAPI, confirmList, failedList } = this.state;
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
        filterdict: filterData,
        CVlist: confirmList,
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
   * @memberOf CVsDocMining
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
      fileList,
      failedList,
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

    const uploadProps = {
      name: 'files',
      action: API.UPLOAD_RESUME_API,
      multiple: true,
      text: '点击或拖曳到此区域',
      hint: '支持单文件或多文件上传',
      onChange: this.handleChange,
      onRemove: this.handleRemove,
    };

    return (
      <div className="cs-fast-matching">
          <Row gutter={24}>
            <Col span={12}>
              <FilterCard
                textarea={textarea}
                onSearch={this.handleSearch}
              />
            </Col>
            <Col span={12}>
              <div className="cs-uploader">
                <ShowCard
                    prefixCls={"cvsdoc-show-card"}>
                  <DraggerUpload
                    {...uploadProps}
                    fileList={fileList}
                    prefixCls={"cvsdoc-upload"}
                  />
                {this.props.children && React.cloneElement(this.props.children, {
                  failedList: failedList,
                  fileList: fileList,
                })}
                </ShowCard>
              </div>
            </Col>
          </Row>
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

CVsDocMining.defaultProps = {
  prefixCls: 'cvdoc-result'
};

export default CVsDocMining;
