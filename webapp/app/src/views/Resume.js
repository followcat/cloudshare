'use strict';
import React, { Component } from 'react';
import Header from '../components/common/Header';
import ResumeItem from '../components/resume/ResumeItem';
import { Tabs, message } from 'antd';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';
import History from '../utils/history';
import { getRadarOption } from '../utils/chart_option';
import generateSummary from '../utils/summary-generator';
import 'whatwg-fetch';
import './resume.less';
const TabPane = Tabs.TabPane;

export default class Resume extends Component {
  constructor() {
    super();
    this.state = {
      currentId: '',
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
    this.getResumeInfoData = this.getResumeInfoData.bind(this);
    this.getPeopleList = this.getPeopleList.bind(this);
    this.getSimilarData = this.getSimilarData.bind(this);
  }

  componentDidMount() {
    const hrefArr = location.href.split('/'),
          id = hrefArr[hrefArr.length-1];

    this.setState({
      currentId: id,
    });

    this.getPeopleList(id);
    this.getResumeInfoData(id);
    this.getSimilarData(id);
  }

  /**
   * 点击Tabs方法
   * @param  {string} key 点击的tab key
   * @return {void}
   */
  handleTabsChange(key) {
    this.setState({
      currentId: key,
    });

    this.getResumeInfoData(key);
    this.getSimilarData(key);
  }

  /**
   * 修改CV title信息方法
   * @param  {object} fieldValue 需要修改的字段对象集合
   * @return {void}
   */
  handleModifyTitle(fieldValue) {
    fetch(`/api/cv/updateinfo`, {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({ id: this.state.currentId, update_info: fieldValue })
    })
    .then(response => response.json())
    .then(json => {
      if(json.code === 200)  {
        message.success(json.message);
        this.getResumeInfoData(this.state.currentId);
      } else {
        message.error(json.message);
      }
    })
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
        bookmark_id: this.state.currentId,
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
        id: this.state.currentId,
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
    fetch(`/api/jdlist`, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData()
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        this.setState({
          jdList: json.data.filter(item => item.status === 'Opening'),
        });
      }
    })
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
          cvId = this.state.currentId;

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
    let tagList = this.state.tag;
    fetch(`/api/cv/updateinfo`, {
      method: 'PUT',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        id: this.state.currentId,
        update_info: fieldValue,
      })
    })
    .then(response => response.json())
    .then(json => {
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
    let followUpList = this.state.tracking;

    fetch(`/api/cv/updateinfo`, {
      method: 'PUT',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        id: this.state.currentId,
        update_info: {
          tracking: fieldValue,
        },
      })
    })
    .then(response => response.json())
    .then(json => {
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
    let commentList = this.state.comment;

    fetch(`/api/cv/updateinfo`, {
      method: 'PUT',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        id: this.state.currentId,
        update_info: fieldValue,
      })
    })
    .then(response => response.json())
    .then(json => {
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
   * 获取简历信息数据
   * @param  {string} id 简历ID值
   * @return {void}
   */
  getResumeInfoData(id) {
    this.setState({
      paneLoading: true,
      html: '',
      enHtml: '',
      dataSource: {},
      collected: false,
      tag: [],
      tracking: [],
      comment: [],
      similar: [],
      radarOption: {},
    });

    fetch(`/api/resume`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({ id: id }),
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        const yamlInfo = json.data.yaml_info;
        this.setState({
          html: json.data.html,
          enHtml: json.data.en_html,
          dataSource: yamlInfo,
          collected: yamlInfo.collected,
          tag: yamlInfo.tag,
          tracking: yamlInfo.tracking,
          comment: yamlInfo.comment,
          paneLoading: false,
        });

        History.write({
          id: id,
          name: yamlInfo.name
        });
      }
    })
  }

  /**
   * 获取与id简历相似的候选人列表
   * @param  {string} id 待匹配的简历id
   * @return {void}
   */
  getSimilarData(id) {
    fetch(`/api/mining/similar`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        id: id
      })
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        this.setState({
          similar: json.data,
        });
      }
    })
  }

  /**
   * 获取候选人所有简历版本列表
   * @param  {string} id 候选人简历ID
   * @return {void}
   */
  getPeopleList(id) {
    fetch(`/api/projuectbyid/${id}`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`,
      }
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        this.setState({
          resumeList: json.data.cv,
        });
      }
    });
  }

  render() {
    const extendInfo = {
      tag: this.state.tag,
      tracking: this.state.tracking,
      comment: this.state.comment,
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
          <Tabs
            type="card"
            activeKey={this.state.currentId}
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
                    paneLoading={this.state.paneLoading}
                    currentId={this.state.currentId}
                    active={this.state.currentId === item}
                    text={`Item: ${item}`}
                    dataSource={this.state.dataSource}
                    summary={generateSummary(this.state.dataSource)}
                    html={this.state.html}
                    enHtml={this.state.enHtml}
                    collected={this.state.collected}
                    upload={uploadProps}
                    fileList={this.state.fileList}
                    jdList={this.state.jdList}
                    radarOption={this.state.radarOption}
                    chartSpinning={this.state.chartSpinning}
                    enComfirmLoading={this.state.enComfirmLoading}
                    extendInfo={extendInfo}
                    similar={this.state.similar}
                    onModifyTitle={this.handleModifyTitle}
                    onCollection={this.handleCollection}
                    onEnComfirmLoading={this.handleEnComfirmLoading}
                    onDrawChartOpen={this.handleDrawChartOpen}
                    onDrawChartSubmit={this.handleDrawChartSubmit}
                    onSubmitTag={this.handleSubmitTag}
                    onSubmitFollowUp={this.handleSubmitFollowUp}
                    onSubmitComment={this.handleComment}
                  />
                </TabPane>
              );
            })}
          </Tabs>
        </div>
      </div>
    );
  }
}