'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import Header from '../components/common/Header';
import Uploader from '../components/upload/Uploader';
import PreviewList from '../components/upload/PreviewList';
import ComfirmResult from '../components/upload/ComfirmResult';
import { message } from 'antd';

import Generator from '../utils/generator';

import './upload.less';

const findIndexOf = (key, object, array) => {
  for (let i = 0, len = array.length; i < len; i++) {
    if (array[i][key] === object[key]) {
      return i;
    }
  }
  return -1;
}

export default class Upload extends Component {

  constructor(props) {
    super(props);

    this.state = {
      fileList: [],
      currentPreview: 0,
      completedFileList: [],
      comfirmList: [],
      loading: false,
      disabled: false,
      classifyList: [],
      comfirmResult: [],
      errorResult: [],
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.handlePrevPreview = this.handlePrevPreview.bind(this);
    this.handleNextPreview = this.handleNextPreview.bind(this);
    this.handleComfirmUpload = this.handleComfirmUpload.bind(this);
    this.isObjectExisted = this.isObjectExisted.bind(this);
    this.loadClassify = this.loadClassify.bind(this);
    this.getComfirmResultRender = this.getComfirmResultRender.bind(this);
  }

  loadClassify() {
    fetch(`/api/additionnames`, {
      method: 'GET',
      headers: {
        'Authorization': `Basic ${localStorage.token}`
      }
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          classifyList: json.data,
        });
      }
    })
  }

  componentDidMount() {
    this.loadClassify();
  }

  handleChange(info) {
    let fileList = info.fileList,
        completedFileList = this.state.completedFileList,
        errorResult = this.state.errorResult;

    fileList = fileList.map((file) => {
      if (file.response && file.status === 'done' && !file.flag) {
        file.flag = true;
        if (file.response.code === 200) {
          fetch(`/api/uploadcv/preview`, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Authorization': `Basic ${localStorage.token}`,
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              filename: file.response.data.filename,
            }),
          })
          .then((response) => {
            return response.json();
          })
          .then((json) => {
            if (json.code === 200) {
              file.response.data = Object.assign(file.response.data, json.data);
              file.filename = json.data.filename;
              completedFileList.push(Object.assign({}, file.response.data, { uid: file.uid }));
              this.setState({
                completedFileList: completedFileList,
              });
            }
          });
        } else {
          message.error(`Upload file ${file.name} failed.`, 3);
          errorResult.push({
            id: '',
            status: 'error',
            message: 'Timeout! System can not parse this file.',
            filename: file.name,
            uid: file.uid,
          });
          this.setState({
            errorResult: errorResult,
          });
        }
      }
      return file;
    });

    this.setState({
      fileList: fileList,
    });
  }

  handleRemove(file) {
    let fileObject = file,
        fileList = this.state.fileList,
        comfirmResult = this.state.comfirmResult,
        completedFileList = this.state.completedFileList,
        errorResult = this.state.errorResult,
        comfirmList = this.state.comfirmList,
        currentPreview = this.state.currentPreview;

    let index = -1;

    index = findIndexOf('uid', fileObject, fileList);
    if (index > -1) {
      fileList.splice(index, 1);
    }

    index = findIndexOf('uid', fileObject, comfirmResult);
    if (index > -1) {
      comfirmResult.splice(index, 1);
    }

    index = findIndexOf('uid', fileObject, completedFileList);
    if (index > -1) {
      completedFileList.splice(index, 1);
      currentPreview--;
    }

    index = findIndexOf('uid', fileObject, errorResult);
    if (index > -1) {
      errorResult.splice(index, 1);
    }

    index = findIndexOf('filename', fileObject, comfirmList);
    if (index > -1) {
      comfirmList.splice(index, 1);
    }

    this.setState({
      fileList: fileList,
      comfirmResult: comfirmResult,
      errorResult: errorResult,
      comfirmList: comfirmList,
      currentPreview: currentPreview < 0 ? 0 : currentPreview,
    });
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (nextState.fileList.length !== this.state.fileList.length) {
      return true;
    }

    if (nextState.fileList.length === nextState.completedFileList.length) {
      return true;
    }

    if (nextState.fileList.length === nextState.errorResult.length) {
      return true; 
    }

    if (nextState.loading !== this.state.loading) {
      return true;
    }

    return false;
  }

  isObjectExisted(array, targetId) {
    for( let item of array) {
      if (item.id === targetId) {
        return true;
      }
    }
    return false;
  }

  handlePrevPreview(value) {
    let current = this.state.currentPreview,
        comfirm = this.state.comfirmList;

    const index = findIndexOf('filename', value, comfirm);
    if (index > -1) {
      comfirm[index] = Object.assign(comfirm[index], value);
    } else {
      comfirm.push(value);
    }

    this.setState({
      currentPreview: current - 1,
      comfirmList: comfirm,
    });
  }

  handleNextPreview(value) {
    let current = this.state.currentPreview,
        comfirm = this.state.comfirmList;

    const index = findIndexOf('filename', value, comfirm);
    if (index > -1) {
      comfirm[index] = Object.assign(comfirm[index], value);
    } else {
      comfirm.push(value);
    }

    this.setState({
      currentPreview: current + 1,
      comfirmList: comfirm,
    });
  }

  handleComfirmUpload(value) {
    let comfirm = this.state.comfirmList;

    if (findIndexOf('filename', value, comfirm) === -1) {
      comfirm.push(value);
    }

    this.setState({
      comfirmList: comfirm,
      loading: true,
      disabled: true,
    });

    fetch(`/api/uploadcv`, {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: Generator.getPostData({
        updates: comfirm
      })
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        this.setState({
          completedFileList: [],
          fileList: [],
          comfirmList: [],
          comfirmResult: json.data,
          loading: false,
          disabled: false,
        });
      }
    })
  }

  getComfirmResultRender() {
    const state = this.state;
    if (state.errorResult.length > 0 && state.errorResult.length === state.fileList.length) {
      return (
        <ComfirmResult
          errorResult={this.state.errorResult}
        />
      );
    } else if (this.state.comfirmResult.length) {
      return (
        <ComfirmResult
          comfirmResult={this.state.comfirmResult}
          errorResult={this.state.errorResult}
        />
      );
    } else {
      return null;
    }
  }

  render() {
    const h = parseInt(document.body.offsetHeight) - 104;

    const uploadProps = {
      name: 'files',
      action: '/api/uploadcv',
      headers: {
        'Authorization': `Basic ${localStorage.token}`
      },
      multiple: true,
      onChange: this.handleChange,
      onRemove: this.handleRemove,
    };

    return (
      <div>
        <Header fixed={true} />
        <div className="container" style={{ minHeight: h }}>
          <Uploader
            uploadProps={uploadProps}
            fileList={this.state.fileList}
          />
          <PreviewList
            previewList={this.state.completedFileList}
            currentPreview={this.state.currentPreview}
            onPrevPreview={this.handlePrevPreview}
            onNextPreview={this.handleNextPreview}
            onComfirmUpload={this.handleComfirmUpload}
            loading={this.state.loading}
            disabled={this.state.disabled}
            classifyList={this.state.classifyList}
          />
          {this.getComfirmResultRender()}
        </div>
        
      </div>
    );
  }
}