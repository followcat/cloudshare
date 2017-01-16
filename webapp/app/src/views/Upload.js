'use strict';
import React, { Component } from 'react';
import Viewport from '../components/viewport';
import Header from '../components/header';
import CommonNavigation from './CommonNavigation';
import Container from '../components/container';
import ShowCard from '../components/show-card';
import DraggerUpload from '../components/dragger-upload';
import UploadPreview from '../components/upload-preview';
import ConfirmResult from '../components/confirm-result';
import { message } from 'antd';
import { getClassify } from '../request/classify';
import { uploadPreview, confirmUpload } from '../request/upload';
import { API } from '../config/api';
import { URL } from '../config/url';
import StorageUtil from '../utils/storage';
import generateSummary from '../utils/summary-generator';
import remove from 'lodash/remove';
import findIndex from 'lodash/findIndex';
import './upload.less';

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

export default class Upload extends Component {
  constructor() {
    super();
    
    this.state = {
      currentPreview: 0,
      total: 0,
      classifyList: [],
      fileList: [],
      completedList: [],
      confirmList: [],
      failedList: [],
      confirmResult: [],
      confirmLoading: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.handlePrevClick = this.handlePrevClick.bind(this);
    this.handleNextClick = this.handleNextClick.bind(this);
    this.handleConfirmClick = this.handleConfirmClick.bind(this);
    this.getClassifyData = this.getClassifyData.bind(this);
    this.getResultColumns = this.getResultColumns.bind(this);
    this.getRenderConfirmResult = this.getRenderConfirmResult.bind(this);
  }

  componentDidMount() {
    this.getClassifyData();
  }

  handleChange(info) {
    let fileList = info.fileList,
        completedList = this.state.completedList,
        failedList = this.state.failedList;

    fileList = fileList.map((file) => {
      if (file.response && file.status === 'done' && !file.completed) {
        file.completed = true;  // 标记已经上传文件, 避免重复请求preview API

        if (file.response.code === 200) {  // 上传成功后,请求预览数据

          /*
           * 请求preview API方法
           */ 
          uploadPreview({
            filename: file.response.data.filename,
          }, (json) => {
            if (json.code === 200) {
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
          message.error(`Upload file ${file.name} failed.`, 3);

          failedList.push({
            id: '',
            status: 'error',
            message: 'Timeout! System can not parse this file.',
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
      confirmResult: [],
    });
  }

  handleRemove(file) {
    let fileList = this.state.fileList,
        completedList = this.state.completedList,
        confirmList = this.state.confirmList,
        failedList = this.state.failedList,
        currentPreview = this.state.currentPreview,
        total = this.state.total,
        index;

    index = findIndex(completedList, (item) => item.uid === file.uid);

    fileList = removeItem('uid', file.uid, fileList);
    completedList = removeItem('uid', file.uid, completedList);
    failedList = removeItem('uid', file.uid, failedList);
    confirmList = removeItem('filename', file.filename, confirmList);

    this.setState({
      fileList: fileList,
      completedList: completedList,
      confirmList: confirmList,
      failedList: failedList,
      currentPreview: currentPreview === index && currentPreview > 0 ? currentPreview - 1 : currentPreview,
      total: total - 1,
    });
  }

  handlePrevClick(value) {
    let currentPreview = this.state.currentPreview;
    const confirmList = this.state.confirmList;

    this.setState({
      currentPreview: currentPreview - 1,
      confirmList: updateConfirmList(value, confirmList),
    });
  }

  handleNextClick(value) {
    let currentPreview = this.state.currentPreview;
    const confirmList = this.state.confirmList;

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

    confirmUpload({
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

  getResultColumns() {
    const columns = [
      {
        title: 'File Name',
        dataIndex: 'filename',
        key: 'filename',
      }, {
        title: 'Status',
        dataIndex: 'status',
        key: 'status',
        render: (text) => (
          text === 'success' ?
              <span style={{ color: 'green' }}>{text}</span> :
              <span style={{ color: 'red' }}>{text}</span>
        )
      }, {
        title: 'Message',
        dataIndex: 'message',
        key: 'message',
        render: (text) => <span>{text}</span>
      }, {
        title: 'Operation',
        key: 'operation',
        render: (record) => {
          return (
            <a
              href={URL.getResumeURL(record.id)}
              target="_blank"
              disabled={record.status !== 'success' ? true : false}
            >
              Check
            </a>
          );
        }
      }
    ];

    return columns;
  }

  getRenderConfirmResult() {
    const columns = this.getResultColumns();
    let failedList = this.state.failedList,
        confirmResult = this.state.confirmResult,
        fileList = this.state.fileList;

    if (failedList.length > 0 && failedList.length === fileList.length) {
      return (
        <ConfirmResult
          columns={columns}
          dataSource={failedList}
        />
      );
    } else if (confirmResult.length > 0) {
      return (
        <ConfirmResult
          columns={columns}
          dataSource={confirmResult.concat(failedList)}
        />
      )
    } else {
      return null;
    }
  }

  render() {
    const uploadProps = {
      name: 'files',
      action: API.UPLOAD_RESUME_API,
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`
      },
      multiple: true,
      onChange: this.handleChange,
      onRemove: this.handleRemove,
      text: 'Click or drag and drop files to upload on this area',
      hint: 'Support single or mutiple upload',
    };

    return (
      <Viewport>
        <Header
          fixed={this.state.completedList.length === 0}
          logoLink={URL.getSearchURL()}
        >
          <CommonNavigation />
        </Header>
        <Container
          prefixCls={this.state.completedList.length > 0 ? "cs-upload-container" : "cs-container"}
        >
          <ShowCard>
            <DraggerUpload
              {...uploadProps}
              fileList={this.state.fileList}
            />
            {this.state.completedList.length > 0 ?
                this.state.completedList.map((item, index) => {
                  return (
                    <UploadPreview
                      key={index}
                      id={item.filename}  // id是标记文件唯一的标准,这里用filename作为辨识
                      resumeID={item.yaml_info.id}
                      currentPreview={this.state.currentPreview}
                      total={this.state.total}
                      index={index}
                      name={item.yaml_info.name}
                      classifyValue={item.yaml_info.classify}
                      classifyList={this.state.classifyList}
                      html={item.markdown || item.html}
                      summary={generateSummary(item.yaml_info)}
                      similarResume={item.cv}
                      confirmLoading={this.state.confirmLoading}
                      onPrevClick={this.handlePrevClick}
                      onNextClick={this.handleNextClick}
                      onConfirmClick={this.handleConfirmClick}
                    />
                  );
                }) :
                null
            }
            {this.getRenderConfirmResult()}
          </ShowCard>
        </Container>
      </Viewport>
    );
  }
}
