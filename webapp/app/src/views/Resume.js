'use strict';
import React, { Component } from 'react';
import Header from '../components/common/Header';
import ResumeItem from '../components/resume/ResumeItem';
import ResumeExtension from '../components/resume/ResumeExtension';
import { Tabs, message } from 'antd';

import {
  getResumeInfo,
  getSimilar,
  getResumeList,
  getAdditionalInfo,
  updateResumeInfo,
  updateAdditionalInfo
} from '../request/resume';
import {
  getJobDescriptionList
} from '../request/jobdescription';

import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import History from '../utils/history';
import { getRadarOption } from '../utils/chart_option';
import generateSummary from '../utils/summary-generator';
import { URL } from '../config/url';
import 'whatwg-fetch';
import './resume.less';
const TabPane = Tabs.TabPane;

export default class Resume extends Component {
  constructor() {
    super();
    this.state = {
      resumeID: '',
      uniqueID: '',
      resumeList: [],
      html: '',
      enHtml: '',
      dataSource: {},
      collected: false,
      tag: [],
      tracking: [],
      comment: [],
      similar: [],
      fileList: [],
      enComfirmLoading: false,
      jdList: [],
      radarOption: {},
      chartSpinning: false,
      paneLoading: false,
    };
    this.handleTabsChange = this.handleTabsChange.bind(this);
    this.handleModifyTitle = this.handleModifyTitle.bind(this);
    this.handleCollection = this.handleCollection.bind(this);
    this.handleEnComfirmLoading = this.handleEnComfirmLoading.bind(this);
    this.handleDrawChartOpen = this.handleDrawChartOpen.bind(this);
    this.handleDrawChartSubmit = this.handleDrawChartSubmit.bind(this);
    this.handleSubmitTag = this.handleSubmitTag.bind(this);
    this.handleSubmitFollowUp = this.handleSubmitFollowUp.bind(this);
    this.handleComment = this.handleComment.bind(this);
    this.handleUploadChange = this.handleUploadChange.bind(this);
    this.handleDownloadClick = this.handleDownloadClick.bind(this);
    this.getResumeDataSource = this.getResumeDataSource.bind(this);
    this.getResumeIDList = this.getResumeIDList.bind(this);
    this.getSimilarDataSource = this.getSimilarDataSource.bind(this);
  }

  componentDidMount() {
    const hrefArr = location.href.split('/'),
          id = hrefArr[hrefArr.length-1];

    this.setState({
      resumeID: id,
    });

    this.getResumeIDList(id);
    this.getResumeDataSource(id);
    this.getSimilarDataSource(id);
  }

  /**
   * 点击Tabs方法
   * @param  {string} key 点击的tab key
   * @return {void}
   */
  handleTabsChange(key) {
    console.log(key);
    this.setState({
      resumeID: key,
    });

    this.getResumeDataSource(key);
    this.getSimilarDataSource(key);
  }

  /**
   * 修改CV title信息方法
   * @param  {object} fieldValue 需要修改的字段对象集合
   * @return {void}
   */
  handleModifyTitle(fieldValue) {
    updateResumeInfo({
      id: this.state.resumeID,
      update_info: fieldValue
    }, json => {
      if(json.code === 200)  {
        message.success(json.message);
        this.getResumeDataSource(this.state.resumeID);
      } else {
        message.error(json.message);
      }
    });
  }

  /**
   * 收藏简历点击事件方法
   * @return {void}
   */
  handleCollection() {
    const collected = this.state.collected,
          apiURL = `/api/accounts/${StorageUtil.get('user')}/bookmark`,
          requestMethod = collected ? 'DELETE' : 'POST';

    fetch(apiURL, {
      method: requestMethod,
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        bookmark_id: this.state.resumeID,
      })
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        this.setState({
          collected: !collected,
        });
      } else {
        message.error(json.message);
      }
    })
  }

    /**
   * 英文简历上传确认事件方法
   * @return {void}
   */
  handleEnComfirmLoading() {
    this.setState({
      enComfirmLoading: true,
    });

    fetch(`/api/uploadengcv`, {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        id: this.state.resumeID,
      })
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200 && json.data.en_html) {
        this.setState({
          enComfirmLoading: false,
          fileList: [],
          enHtml: json.data.en_html,
        });
      } else {
        this.setState({
          enComfirmLoading: false,
          fileList: [],
        });
        message.error('English CV Comfirm Faild.')
      }
    })
  }

  /**
   * 画图功能模态框开启事件方法,请求JD API
   * @return {void}
   */
  handleDrawChartOpen() {
    getJobDescriptionList(json => {
      if (json.code === 200) {
        this.setState({
          jdList: json.data.filter(item => item.status === 'Opening'),
        });
      }
    });
  }

  /**
   * 绘画候选人雷达图
   * @param  {object} object 传入数据对象
   * @return {void} 
   */
  handleDrawChartSubmit(object, anonymized) {
    if (!object.value) {
      message.error('Please select a job description!');
      return;
    }

    this.setState({
      chartSpinning: true,
    });

    const requestParam = object.type === 'id' ? { id: object.value } : { doc: object.value },
          cvId = this.state.resumeID;

    fetch(`/api/mining/valuable`, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData(Object.assign(requestParam, {
        name_list: [`${cvId}.md`],
      }))
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        const option = getRadarOption(json.data.max, json.data.result, anonymized);
        this.setState({
          radarOption: option,
          chartSpinning: false,
        });
      }
    });
  }

  /**
   * 增加简历标签事件方法
   * @param  {object} fieldValue 表单数据对象
   * @return {void}
   */
  handleSubmitTag(fieldValue) {
    let tagList = this.state.tag,
        uniqueID = this.state.uniqueID;

    updateAdditionalInfo({
      unique_id: uniqueID,
      update_info: fieldValue
    }, json => {
      if (json.code === 200) {
        tagList.push(json.data);
        this.setState({
          tag: tagList,
        });
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  /**
   * 增加跟进内容事件方法
   * @return {object} fieldValue 跟进表单数据对象
   */
  handleSubmitFollowUp(fieldValue) {
    let followUpList = this.state.tracking,
        uniqueID = this.state.uniqueID;

    updateAdditionalInfo({
      unique_id: uniqueID,
      update_info: {
        tracking: fieldValue
      }
    }, json => {
      if (json.code === 200) {
        followUpList.unshift(json.data);
        this.setState({
          tracking: followUpList,
        });
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  /**
   * 增加评论内容事件方法
   * @param  {object} fieldValue 评论表单数据对象
   * @return {void}
   */
  handleComment(fieldValue) {
    let commentList = this.state.comment,
        uniqueID = this.state.uniqueID;

    updateAdditionalInfo({
      unique_id: uniqueID,
      update_info: fieldValue
    }, json => {
      if (json.code === 200) {
        commentList.unshift(json.data);
        this.setState({
          comment: commentList,
        });
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    });
  }

  /**
   * 上传英文简历事件方法
   * @return {[object]} info [上传组件对象]
   * @return {[void]}
   */
  handleUploadChange(info) {
    let fileList = info.fileList;
    fileList = fileList.map((file) => {
      if (file.response) {
        file.url = file.response.data.url;
      }
      return file;
    });
    if (info.file.status === 'done') {
      message.success(`${info.file.name} Upload success.`);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} Upload faild.`);
    }

    this.setState({ fileList });
  }

  /**
   * 简历下载链接
   * @param  {string} id  简历ID
   * @return {void}
   */
  handleDownloadClick(id) {
    location.href = URL.getDownloadURL(id);
  }

  /**
   * 获取简历信息数据
   * @param  {string} id 简历ID值
   * @return {void}
   */
  getResumeDataSource(id) {
    this.setState({
      paneLoading: true,
      html: '',
      enHtml: '',
      dataSource: {},
      collected: false,
      similar: [],
      radarOption: {},
    });

    getResumeInfo({
      id: id
    }, json => {
      if (json.code === 200) {
        const { html, en_html, yaml_info } = json.data,
              uniqueID = yaml_info.unique_id;

        this.setState({
          html: html,
          enHtml: en_html,
          dataSource: yaml_info,
          uniqueID: uniqueID,
          collected: yaml_info.collected,
          paneLoading: false,
        });

        History.write({
          id: id,
          name: yaml_info.name
        });
      }
    });
  }

  /**
   * 获取与id简历相似的候选人列表
   * @param  {string} id 待匹配的简历id
   * @return {void}
   */
  getSimilarDataSource(id) {
    getSimilar({
      id: id
    }, json => {
      if (json.code === 200) {
        this.setState({
          similar: json.data,
        });
      }
    });
  }

  /**
   * 获取候选人所有简历版本列表
   * @param  {string} id 候选人简历ID
   * @return {void}
   */
  getResumeIDList(id) {
    getResumeList({
      cv_id: id
    }, json => {
      if (json.code === 200) {
        const data = json.data;

        this.setState({
          resumeList: data.cv,
          tag: data.tag,
          comment: data.comment,
          tracking: data.tracking
        });
      }
    });
  }

  render() {
    const state = this.state;
          
    const extendInfo = {
      tag: state.tag,
      tracking: state.tracking,
      comment: state.comment,
    };

    const uploadProps = {
      name: 'file',
      action: '/api/uploadengcv',
      headers: {
        Authorization: `Basic ${StorageUtil.get('token')}`,
      },
      onChange: this.handleUploadChange,
    };

    return (
      <div>
        <Header fixed={false} />
        <div className="cs-layout-container">
          <div className="cs-layout-tabs">
            <Tabs
              type="card"
              activeKey={this.state.resumeID}
              onChange={this.handleTabsChange}
            >
              {this.state.resumeList.map(item => {
                return (
                  <TabPane 
                    tab={`ID: ${item}`}
                    key={item}
                  >
                    <ResumeItem
                      key={item}
                      id={item}
                      paneLoading={state.paneLoading}
                      resumeID={state.resumeID}
                      active={state.resumeID === item}
                      text={`Item: ${item}`}
                      dataSource={state.dataSource}
                      summary={generateSummary(state.dataSource)}
                      html={state.html}
                      enHtml={state.enHtml}
                      collected={state.collected}
                      upload={uploadProps}
                      fileList={state.fileList}
                      jdList={state.jdList}
                      radarOption={state.radarOption}
                      chartSpinning={state.chartSpinning}
                      enComfirmLoading={state.enComfirmLoading}
                      onModifyTitle={this.handleModifyTitle}
                      onCollection={this.handleCollection}
                      onEnComfirmLoading={this.handleEnComfirmLoading}
                      onDrawChartOpen={this.handleDrawChartOpen}
                      onDrawChartSubmit={this.handleDrawChartSubmit}
                      onDownloadClick={this.handleDownloadClick}
                    />
                  </TabPane>
                );
              })}
            </Tabs>
          </div>
          <ResumeExtension
            dataSource={extendInfo}
            similar={state.similar}
            onSubmitTag={this.handleSubmitTag}
            onSubmitFollowUp={this.handleSubmitFollowUp}
            onSubmitComment={this.handleComment}
          />
        </div>
      </div>
    );
  }
}