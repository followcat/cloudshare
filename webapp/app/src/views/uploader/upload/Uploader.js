'use strict';
import React, { Component, PropTypes } from 'react';
import { browserHistory } from 'react-router';

import ShowCard from 'components/show-card';
import DraggerUpload from 'components/dragger-upload';
import Preview from './Preview';

import { message } from 'antd';

import { getClassify } from 'request/classify';
import { uploadPreview, confirmUpload } from 'request/upload';

import { API } from 'API';

import StorageUtil from 'utils/storage';

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
      currentPreview: 0,
      total: 0,
      confirmLoading: false
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.handlePrevClick = this.handlePrevClick.bind(this);
    this.handleNextClick = this.handleNextClick.bind(this);
    this.handleConfirmClick = this.handleConfirmClick.bind(this);
    this.getClassifyData = this.getClassifyData.bind(this);
    this.getPreviewRender = this.getPreviewRender.bind(this);
  }

  componentDidMount() {
    this.getClassifyData();
  }

  handleChange(info) {
    let fileList = info.fileList,
        { completedList, failedList } = this.state;

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

              completedList.push(Object.assign({}, file.response.data, { uid: file.uid }));
              
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
          pathname: '/uploader/upload/result'
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
      confirmLoading
    } = this.state;

    if (completedList.length > 0) {
      return (
        <Preview
          completedList={completedList}
          classifyList={classifyList}
          currentPreview={currentPreview}
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
      confirmResult
    } = this.state;

    const uploadProps = {
      name: 'files',
      action: API.UPLOAD_RESUME_API,
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`
      },
      multiple: true,
      text: '点击或拖曳到此区域',
      hint: '支持单文件或多文件上传',
      onChange: this.handleChange,
      onRemove: this.handleRemove,
    };

    return (
      <div className="cs-uploader">
        <ShowCard>
          <DraggerUpload
            {...uploadProps}
            fileList={fileList}
          />
          {this.getPreviewRender()}
          {this.props.children && React.cloneElement(this.props.children, {
            completedList: completedList,
            failedList: failedList,
            fileList: fileList,
            confirmResult: confirmResult
          })}
        </ShowCard>
      </div>
    );
  }
}

Uploader.propTypes = {
  children: PropTypes.oneOfType([PropTypes.element, PropTypes.array])
};

export default Uploader;
