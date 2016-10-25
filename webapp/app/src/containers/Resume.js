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
    };

    this.loadData = this.loadData.bind(this);
    this.handleModifyTitle = this.handleModifyTitle.bind(this);
    this.handleCollection = this.handleCollection.bind(this);
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
        this.setState({
          html: json.data.html,
          dataSource: json.data.yaml_info,
          collected: json.data.yaml_info.collected,
        });
      }
    })
  }

  componentDidMount() {
    const hrefArr = location.href.split('/'),
          id = hrefArr[hrefArr.length-1];
    this.setState({
      id: id,
    });
    this.loadData(id);
  }

  render() {
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
        </div>
      </div>
    );
  }
}