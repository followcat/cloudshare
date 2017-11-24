'use strict';
import React, { Component, PropTypes } from 'react';
import { browserHistory } from 'react-router';

import ShowCard from 'components/show-card';
import DraggerUpload from 'components/dragger-upload';
import Guide from 'components/guide';
import Summary from 'components/summary';
import SearchResultBox from 'components/jd-search-result-box';

import Preview from './Preview';

import { message } from 'antd';

import { introJs } from 'intro.js';

import { jdMatching, proJdMatching } from 'request/matching';
import { getClassify } from 'request/classify';
import { uploadPreview, confirmUpload } from 'request/upload';
import { getUploadOrigin } from 'request/classify';
import { getPeopleID } from 'request/account';
import {  getResumeInfo } from 'request/resume';

import { API } from 'API';

import StorageUtil from 'utils/storage';
import { generateSummary } from 'utils/summary-generator';

import remove from 'lodash/remove';
import findIndex from 'lodash/findIndex';

/*
 * 更新confirm列表数据
 * @param  {object} value       表单值
 * @param  {array} confirmList  确认上传列表
 * @return {array} confirmList 返回更新数据后的确认上传列表
 */
const updateConfirmList = (value, confirmList) => {
  const index = findIndex(confirmList, (item) => item.filename === value.id);

  if (index > -1) {
    Object.assign(confirmList[index], { filename: value.id }, value.fieldsValue);
  } else {
    confirmList.push(Object.assign({}, { filename: value.id }, value.fieldsValue));
  }

  return confirmList;
};

/*
 * 删除数组元素
 * @param  {string}        key    需要进行匹配的对象属性
 * @param  {string|number} value  属性值
 * @param  {array}         array  目标数组列表
 * @return {array}                返回删除后的新数组
 */
const removeItem = (key, value, array) => {
  return remove(array, (item) => {
    return item[key] !== value;
  });
};

class Uploader extends Component {
  constructor() {
    super();
    this.state = {
      fileList: [],
      completedList: [],
      confirmList: [],
      failedList: [],
      classifyList: [],
      confirmResult: [],
      yaml_info: [],
      origins: [],
      origin: '',
      peopleid: '',
      totals: 0,
      currentPreview: 0,
      total: 0,
      guide:false,
      getproend: false,
      confirmLoading: false,
      setpeople: false
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleChangeOrigin = this.handleChangeOrigin.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.handlePrevClick = this.handlePrevClick.bind(this);
    this.handleNextClick = this.handleNextClick.bind(this);
    this.handleConfirmClick = this.handleConfirmClick.bind(this);
    this.getClassifyData = this.getClassifyData.bind(this);
    this.getPreviewRender = this.getPreviewRender.bind(this);
  }

  componentWillMount() {

    getPeopleID((json) => {
      if (json.code === 200) {
        this.setState({
          peopleid: json.result.cv[0],
        },() => {this.getProResume()});
      } 
    });

    getUploadOrigin((json) => {
      if (json.code === 200) {
        this.setState({
          origins: json.data,
        });
      }
    });

    proJdMatching({
      'page': `page=0`,
      'numbers': `numbers=3`
    }, json => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
        });
      }
    });

    if(this.props.location.query.guide) {
      this.setState({
      guide: this.props.location.query.guide
      })
    }
  }

  componentDidMount() {
    this.getClassifyData();
    if(this.state.guide) {
      introJs().setOptions({
        'skipLabel': '退出', 
        'prevLabel':'上一步', 
        'nextLabel':'下一步',
        'doneLabel': '完成'
      }).start();
      // introJs().start();
    }
    // this.getProResume();
  }

  componentDidUpdate() {
    if(this.state.peopleid&&!this.state.getproend)  {
      // this.getProResume()
    }
  }

  getProResume() {
    getResumeInfo({
      id: this.state.peopleid
      }, json => {
        if (json.code === 200) {
            this.setState({
              yaml_info: json.data.yaml_info,
              getproend: true
            });
        }
      });
  }

  handleChangeOrigin(origin) {
    this.setState({
      origin: origin
    });
  }

  handleChange(info) {
    let fileList = info.fileList,
        { completedList, failedList } = this.state;

        fileList = fileList.slice(-1);

    fileList = fileList.map(file => {
      if (file.response && file.status === 'done' && !file.completed) {
        file.completed = true;  // 标记已经上传文件, 避免重复请求preview API

        if (file.response.code === 200) {  // 上传成功后,请求预览数据
          // 请求preview API方法
          uploadPreview(API.UPLOAD_RESUME_PREVIEW_API, {
            filename: file.response.data.filename
          }, json => {
            if (json.code === 200) {
              file.status = 'done';
              file.response.data = Object.assign({}, file.response.data, json.data);
              file.filename = json.data.filename;

              completedList.push(Object.assign({}, file.response.data,
                { uid: file.uid }));

              completedList = completedList.slice(-1);
              
              this.setState({
                completedList: completedList,
                total: completedList.length,
              });
            }
          });
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

          this.setState({
            failedList: failedList,
          });
        }
      }

      return file;
    });

    this.setState({
      fileList: fileList,
      confirmResult: []
    });
  }

  handleRemove(file) {
    let {
      completedList,
      confirmList,
      failedList,
      currentPreview,
      total
    } = this.state,
      index = null;

    index = findIndex(completedList, item => item.uid === file.uid);
    completedList = removeItem('uid', file.uid, completedList);
    failedList = removeItem('uid', file.uid, failedList);
    confirmList = removeItem('filename', file.filename, confirmList);

    this.setState({
      completedList: completedList,
      confirmList: confirmList,
      failedList: failedList,
      currentPreview: currentPreview === index && currentPreview > 0 ? currentPreview - 1 : currentPreview,
      total: total - 1
    });
  }

  handlePrevClick(value) {
    let { currentPreview, confirmList } = this.state;

    this.setState({
      currentPreview: currentPreview - 1,
      confirmList: updateConfirmList(value, confirmList),
    });
  }

  handleNextClick(value) {
    let { currentPreview, confirmList } = this.state;

    this.setState({
      currentPreview: currentPreview + 1,
      confirmList: updateConfirmList(value, confirmList),
    });
  }

  handleConfirmClick(value) {

    const confirmList = updateConfirmList(value, this.state.confirmList);

    this.setState({
      confirmList: confirmList,
      confirmLoading: true,
    });

    confirmUpload(API.UPLOAD_RESUME_API, {
      setpeople: true,
      updates: confirmList
    }, (json) => {
      if (json.code === 200) {
        this.setState({
          completedList: [],
          fileList: [],
          confirmList: [],
          confirmResult: json.data,
          currentPreview: 0,
          total: 0,
          confirmLoading: false,
        });

        browserHistory.push({
          pathname: '/prouploader/upload/result'
        });
      }
    });
  }

  getClassifyData() {
    getClassify(json => {
      if (json.code === 200) {
        this.setState({
          classifyList: json.data,
        });
      }
    });
  }

  getPreviewRender() {
    const {
      completedList,
      classifyList,
      currentPreview,
      total,
      origin,
      origins,
      peopleid,
      confirmLoading
    } = this.state;

    if (completedList.length > 0) {
      return (
        <Preview
          peopleid={peopleid}
          completedList={completedList}
          classifyList={classifyList}
          currentPreview={currentPreview}
          origins={origins}
          defaultOrigin={origin}
          total={total}
          confirmLoading={confirmLoading}
          onPrevClick={this.handlePrevClick}
          onNextClick={this.handleNextClick}
          onConfirmClick={this.handleConfirmClick}
        />
      );
    }

    return null;
  }

  render() {
    const {
      fileList,
      completedList,
      failedList,
      confirmResult,
      guide,
      origins,
      totals,
      dataSource,
      yaml_info
    } = this.state;

    const uploadProps = {
      name: 'files',
      action: API.UPLOAD_RESUME_API,
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`
      },
      origins: origins,
      multiple: false,
      text: '点击上传或拖放文件到此区域',
      hint: '只支持单文件上传',
      onChange: this.handleChange,
      onRemove: this.handleRemove,
    };

    return (
      <div className="cs-uploader" >
        <Guide />
        <ShowCard>
        <div data-step='1'data-intro='单击或拖放文件上传!'>
          <DraggerUpload
            {...uploadProps}
            fileList={fileList}
            handleChangeOrigin={this.handleChangeOrigin}
          />
          </div>
          {guide ?
          <div className="cs-uploader-steptwo" data-step='2' data-intro='上传成功后在这里预览文件!'>
          </div>
          : null
          }
          {this.getPreviewRender()}
          {this.props.children && React.cloneElement(this.props.children, {
            completedList: completedList,
            failedList: failedList,
            fileList: fileList,
            confirmResult: confirmResult
          })}
          { dataSource ?
            <div>
            { (completedList.length==0) ?
              <div>
                <div className="cs-uploader-preview">
                <Summary dataSource={generateSummary(yaml_info)} />
                </div>
                <SearchResultBox
                  visible={true}
                  current={0}
                  total={totals}
                  spinning={false}
                  showPagination={false}
                  dataSource={dataSource}
                  educationExperienceText="教育经历"
                  workExperienceText="工作经历"
                  foldText="展开"
                  unfoldText="收起"
                />
              </div>
              : null
            } 
          </div>
          :
          null
          }
        </ShowCard>
      </div>
    );
  }
}

Uploader.propTypes = {
  children: PropTypes.oneOfType([PropTypes.element, PropTypes.array])
};

export default Uploader;
