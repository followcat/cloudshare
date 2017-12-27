'use strict';
import React, { Component } from 'react';
import { browserHistory } from 'react-router';

import { Layout } from 'views/layout';

import ResumeContent from 'components/resume-content';
import ResumeTemplate from 'components/resume-template';
import Summary from 'components/summary';

import ResumeHeader from './ResumeHeader';
import ResumeToolMenu from './ResumeToolMenu';
import ResumeTag from './ResumeTag';
import ResumeFollowUp from './ResumeFollowUp';
import ResumeComment from './ResumeComment';
import ResumeSimilar from './ResumeSimilar';

import {
  Tabs,
  Tag,
  Spin,
  message,
  Card
} from 'antd';

import {
  updateResumeInfo,
  updateAdditionalInfo,
  getResumeInfo,
  getResumeList,
  getSimilar
} from 'request/resume';
import { addBookmark, deleteBookmark } from 'request/bookmark';
import { confirmUpload } from 'request/upload';
import { getHlighLight, getHlighLightKeyWord, getHlighLightDoc } from 'request/highlight';

import { API } from 'API';
import { URL } from 'URL';

import { generateSummary } from 'utils/summary-generator';
import History from 'utils/history';
import StorageUtil from 'utils/storage';

class Resume extends Component {
  constructor(props) {
    super(props);
    this.state = {
      uniqueId: '',
      resumeId: '',
      jd: '',
      searchText: '',
      matchDoc: '',
      resumeList: [],
      fileList: [],
      dataSource: null,
      html: '',
      enHTML: '',
      project: [],
      collected: false,
      panelLoading: false,
      confirmLoading: false,
      highlight: [],
      tag: [],
      tracking: [],
      comment: [],
      similar: []
    };
    this.handleTabsChange = this.handleTabsChange.bind(this);
    this.handleCollection = this.handleCollection.bind(this);
    this.handleSubmitModification = this.handleSubmitModification.bind(this);
    this.handleSubmitTag = this.handleSubmitTag.bind(this);
    this.handleSubmitFollowUp = this.handleSubmitFollowUp.bind(this);
    this.handleComment = this.handleComment.bind(this);
    this.handleUploadChange = this.handleUploadChange.bind(this);
    this.handleUploadModalOk = this.handleUploadModalOk.bind(this);
    this.getResumeDataSource = this.getResumeDataSource.bind(this);
    this.getResumeIDList = this.getResumeIDList.bind(this);
    this.getHlighLightData = this.getHlighLightData.bind(this);
    this.getHlighLightKeyWord = this.getHlighLightKeyWord.bind(this);
    this.getHlighLightByDoc = this.getHlighLightByDoc.bind(this);
    this.getSimilarDataSource = this.getSimilarDataSource.bind(this);
    this.handSelectProject = this.handSelectProject.bind(this);
  }

  componentWillMount() {
    const { jd_id, search_text, match_doc } 
          = this.props.location.query;
    const id = this.props.params.resumeId;
    const jdid = jd_id,
  searchText = search_text,
    matchDoc = match_doc;

    this.setState({
      resumeId: id,
            jd: jdid,
    searchText: searchText,
      matchDoc: matchDoc
    });

    this.getResumeDataSource(id);
    this.getResumeIDList(id);
    if(jdid)
    this.getHlighLightData(jdid,id,30);
    if(searchText)
    this.getHlighLightKeyWord(searchText);
    matchDoc && this.getHlighLightByDoc(matchDoc,id,30);
    this.getSimilarDataSource(id);
  }

  handSelectProject(e){
    const { project } = this.state;
    StorageUtil.set('_pj',e.target.innerText);
    window.location.reload();
  }

  /**
   * 点击Tabs事件方法
   * 
   * @param {any} key 
   * 
   * @memberOf Resume
   */
  handleTabsChange(key) {
    this.setState({
      resumeId: key
    });
    browserHistory.push(`/resume/${key}`);
    this.getResumeDataSource(key);
    this.getSimilarDataSource(key);
  }

  /**
   * 收藏简历点击事件方法
   * 
   * @memberOf Resume
   */
  handleCollection() {
    const { resumeId, collected } = this.state;

    if (collected) {
      deleteBookmark({
        bookmark_id: resumeId
      }, json => {
        if (json.code === 200) {
          this.setState({
            collected: !collected
          });
        } else {
          message.error('操作失败!');
        }
      });
    } else {
      addBookmark({
        bookmark_id: resumeId
      }, json => {
        if (json.code === 200) {
          this.setState({
            collected: !collected
          });
        } else {
          message.error('操作失败!');
        }
      });
    }
  }

  handleSubmitModification(fieldValue) {
    const { resumeId } = this.state;

    updateResumeInfo({
      id: resumeId,
      update_info: fieldValue
    }, json => {
      if(json.code === 200)  {
        message.success('操作成功!');
        this.getResumeDataSource(resumeId);
      } else {
        message.error('操作失败!');
      }
    });
  }

  /**
   * 增加简历标签事件方法
   * 
   * @param {object} fieldValue 
   * 
   * @memberOf Resume
   */
  handleSubmitTag(fieldValue) {
    const { tag, uniqueId } = this.state;

    updateAdditionalInfo({
      unique_id: uniqueId,
      update_info: fieldValue
    }, json => {
      if (json.code === 200) {
        tag.push(json.data);
        this.setState({ tag });

        message.success('添加成功!');
      } else {
        message.error('添加失败!');
      }
    });
  }

  /**
   * 增加跟进内容事件方法
   * 
   * @param {object} fieldValue 
   * 
   * @memberOf Resume
   */
  handleSubmitFollowUp(fieldValue) {
    const { tracking, uniqueId } = this.state;

    updateAdditionalInfo({
      unique_id: uniqueId,
      update_info: {
        tracking: fieldValue
      }
    }, json => {
      if (json.code === 200) {
        tracking.unshift(json.data);
        this.setState({ tracking });

        message.success('添加成功!');
      } else {
        message.error('添加失败!');
      }
    });
  }

  /**
   * 增加评论内容事件方法
   * 
   * @param {object} fieldValue 
   * 
   * @memberOf Resume
   */
  handleComment(fieldValue) {
    const { comment, uniqueId } = this.state;

    updateAdditionalInfo({
      unique_id: uniqueId,
      update_info: fieldValue
    }, json => {
      if (json.code === 200) {
        comment.unshift(json.data);
        this.setState({ comment });

        message.success('添加成功!');
      } else {
        message.error('添加失败!');
      }
    });
  }

  handleUploadChange(info) {
    let fileList = info.fileList;
    fileList = fileList.map((file) => {
      if (file.response) {
        file.url = URL.getPreview();
      }
      return file;
    });
    if (info.file.status === 'done') {
      message.success(`上传${info.file.name}成功.`);
    } else if (info.file.status === 'error') {
      message.error(`上传${info.file.name}失败.`);
    }

    this.setState({ fileList });
  }

  /**
   * 确认上传文件按钮事件
   * 
   * 
   * @memberOf Resume
   */
  handleUploadModalOk() {
    const { resumeId } = this.state;

    this.setState({
      confirmLoading: true
    });

    confirmUpload(API.UPLOAD_ENGLISH_RESUME_API, {
      id: resumeId
    }, json => {
      if (json.code === 200 && json.data.en_html) {
        this.setState({
          confirmLoading: false,
          fileList: [],
          enHTML: json.data.en_html,
        });
        message.error('上传英文简历成功!');
      } else {
        this.setState({
          confirmLoading: false,
          fileList: [],
        });
        message.error('上传英文简历失败!');
      }
    });
  }

  /**
   * 获取简历信息数据
   * 
   * @param {string} id 
   * 
   * @memberOf Resume
   */
  getResumeDataSource(id) {
    this.setState({
      panelLoading: true
    });

    getResumeInfo({
      id: id
    }, json => {
      if (json.code === 200) {
        const { html, en_html, yaml_info, projects } = json.data;
        
        this.setState({
          html: html,
          enHTML: en_html,
          dataSource: yaml_info,
          collected: yaml_info.collected,
          panelLoading: false,
          project: projects
        });
        History.write({
          id: id,
          name: yaml_info.name
        });
      }
    });
  }

    /**
   * 获取jd和cv之间支撑词
   * 
   * @param {string} jd ,{string} cv ,{int} top
   * 
   * @memberOf Resume
   */
  getHlighLightData(jd,cv,top) {
    getHlighLight({
      jd: jd,
      cv: cv,
     top: top,
    }, json => {
      if (json.code === 200) {
        this.setState({
          highlight: json.data,
        });
      }
    });
   }

    /**
   * 获取keyword highlight
   * 
   * @param {string} keyword
   * 
   * @memberOf Resume
   */
  getHlighLightKeyWord(searchText) {
    getHlighLightKeyWord({
      keyword: searchText
    }, json => {
      if (json.code === 200) {
        this.setState({
          highlight: json.data,
        });
      }
    });
   }

    /**
   * 获取doc match highlight
   * 
   * @param {string} doc ,{string} cv ,{int} top
   * 
   * @memberOf Resume
   */
  getHlighLightByDoc(doc,cv,top) {
    getHlighLightDoc({
      cv: cv,
      top: top,
      doc: doc
    }, json => {
      if (json.code === 200) {
        this.setState({
          highlight: json.data,
        });
      }
    });
   }

  /**
   * 获取候选人所有简历版本列表
   * 
   * @param {string} id  
   *         
   * 
   * @memberOf Resume
   */
  getResumeIDList(id) {
    getResumeList({
      cv_id: id
    }, json => {
      if (json.code === 200) {
        const data = json.data;

        this.setState({
          uniqueId: data.id,
          resumeList: data.cv,
          tag: data.tag,
          comment: data.comment,
          tracking: data.tracking
        });
      }
    });
  }

  /**
   * 获取与id简历相似的候选人列表
   * 
   * @param {string} id 
   * 
   * @memberOf Resume
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
  render() {
    const {
      resumeId,
      uniqueId,
      dataSource,
      collected,
      resumeList,
      fileList,
      panelLoading,
      searchText,
      highlight,
      html,
      enHTML,
      tag,
      tracking,
      comment,
      similar,
      project
    } = this.state;
    const uploadProps = {
      name: 'file',
      action: API.UPLOAD_ENGLISH_RESUME_API,
      headers: {
        Authorization: `Basic ${StorageUtil.get('token')}`,
      },
      onChange: this.handleUploadChange,
    };
    return (
      <Layout>
        <div className="cs-layout-resume">
          <div className="cs-layout-tabs">
            <Tabs
              type="card"
              activeKey={resumeId}
              onChange={this.handleTabsChange}
            >
              {resumeList.map(item => {
                return (
                  <Tabs.TabPane tab={`ID: ${item}`} key={item}>
                    <Spin spinning={panelLoading}>
                      <div className="cs-resume-wrapper">
                        <ResumeHeader 
                          collected={collected}
                          dataSource={dataSource}
                          onCollection={this.handleCollection}
                        />
                        <div className="cv-resume-content">
                          <ResumeToolMenu
                            resumeId={resumeId}
                            dataSource={dataSource}
                            uploadProps={uploadProps}
                            fileList={fileList}
                            onSubmitModification={this.handleSubmitModification}
                            onUploadModalOk={this.handleUploadModalOk}
                          />
                          <Summary dataSource={generateSummary(dataSource)} />
                          <Tabs defaultActiveKey="chinese">
                            <Tabs.TabPane tab="中文" key="chinese">
                            { dataSource &&
                              <ResumeTemplate 
                                dataSource={dataSource}
                                searchText={searchText}
                                highlight={highlight}
                              />
                            }
                            </Tabs.TabPane>
                            <Tabs.TabPane tab="原文" key="html">
                              <ResumeContent html={html} />
                            </Tabs.TabPane>
                            <Tabs.TabPane
                              tab="English"
                              key="english"
                              disabled={!enHTML}
                            >
                              <ResumeContent html={enHTML} />
                            </Tabs.TabPane>
                          </Tabs>
                        </div>
                      </div>
                    </Spin>
                  </Tabs.TabPane>
                );
              })}
            </Tabs>
          </div>
          <div className="resume-side">
            <Card title="所属项目">
            { project.map(item => {
                return (
                  <Tag color="blue" onClick={this.handSelectProject}>{item}</Tag>
                  );
              })
            }
            </Card>
            <ResumeTag dataSource={tag} uniqueId={uniqueId} onSubmitTag={this.handleSubmitTag} />
            <ResumeFollowUp dataSource={tracking} onSubmitFollowUp={this.handleSubmitFollowUp} />
            <ResumeComment dataSource={comment} onSubmitComment={this.handleComment} />
            <ResumeSimilar dataSource={similar} id={resumeId}/>
          </div>
        </div>
      </Layout>
    );
  }
}

export default Resume;
