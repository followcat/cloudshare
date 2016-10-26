'use strict';
import React, { Component } from 'react';

import { message } from 'antd';

import Header from '../components/common/Header';
import ResumeWrapper from '../components/resume/ResumeWrapper';
import ResumeExtension from '../components/resume/ResumeExtension';

import 'whatwg-fetch';
import StorageUtil from '../utils/storage';
import Generator from '../utils/generator';

import './resume.less';

export default class Resume extends Component {

  constructor() {
    super();

    this.state = {
      id: '',
      html: '',
      dataSource: {},
      collected: false,
      tag: [],
      tracking: [],
      comment: [],
      similar: [],
    };

    this.loadData = this.loadData.bind(this);
    this.loadSimilarData = this.loadSimilarData.bind(this);
    this.handleModifyTitle = this.handleModifyTitle.bind(this);
    this.handleCollection = this.handleCollection.bind(this);
    this.handleSubmitTag = this.handleSubmitTag.bind(this);
    this.handleSubmitFollowUp = this.handleSubmitFollowUp.bind(this);
    this.handleComment = this.handleComment.bind(this);
  }

  /**
   * 修改CV title信息方法
   * @param  {[object]} fieldValue [需要修改的字段对象集合]
   * @return {[void]}
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
      body: Generator.getPostData({ id: this.state.id, update_info: fieldValue })
    })
    .then(response => response.json())
    .then(json => {
      if(json.code === 200)  {
        message.success(json.message);
      } else {
        message.error(json.message);
      }
    })
  }

  /**
   * 收藏简历点击事件方法
   * @return {[void]}
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
        bookmark_id: this.state.id,
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
   * 增加简历标签事件方法
   * @param  {[object]} fieldValue [表单数据对象]
   * @return {[void]}
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
        id: this.state.id,
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
      } else {
        message.error(json.message);
      }
    })
  }

  /**
   * 增加跟进内容事件方法
   * @return {[object]} fieldValue [跟进表单数据对象]
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
        id: this.state.id,
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
      } else {
        message.error(json.message);
      }
    })
  }

  /**
   * 增加评论内容事件方法
   * @param  {[object]} fieldValue [评论表单数据对象]
   * @return {[void]}
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
        id: this.state.id,
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
      } else {
        message.error(json.message);
      }
    })
  }

  /**
   * 初始加载简历信息数据
   * @param  {[string]} id [简历ID值]
   * @return {[void]}
   */
  loadData(id) {
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
          dataSource: yamlInfo,
          collected: yamlInfo.collected,
          tag: yamlInfo.tag,
          tracking: yamlInfo.tracking,
          comment: yamlInfo.comment,
        });
      }
    })
  }

  /**
   * 获取与id简历相似的候选人列表
   * @param  {[string]} id [待匹配的简历id]
   * @return {[void]}
   */
  loadSimilarData(id) {
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

  componentDidMount() {
    const hrefArr = location.href.split('/'),
          id = '03owtfzq';
          // id = hrefArr[hrefArr.length-1];
    this.setState({
      id: id,
    });
    this.loadData(id);
    this.loadSimilarData(id);
  }

  render() {
    const extendInfo = {
      tag: this.state.tag,
      tracking: this.state.tracking,
      comment: this.state.comment,
    };

    return (
      <div>
        <Header fixed={false} />
        <div className="cs-layout-container">
          <ResumeWrapper
            dataSource={this.state.dataSource}
            html={this.state.html}
            onModifyTitle={this.handleModifyTitle}
            collected={this.state.collected}
            onCollection={this.handleCollection}
          />
          <ResumeExtension
            dataSource={extendInfo}
            similar={this.state.similar}
            onSubmitTag={this.handleSubmitTag}
            onSubmitFollowUp={this.handleSubmitFollowUp}
            onSubmitComment={this.handleComment}
          />
        </div>
      </div>
    );
  }
}