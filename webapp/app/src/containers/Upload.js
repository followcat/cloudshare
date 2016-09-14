'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import Header from '../components/common/Header';
import Uploader from '../components/upload/Uploader';
import PreviewList from '../components/upload/PreviewList';
import ComfirmResult from '../components/upload/ComfirmResult';

import './upload.less';

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
    };

    this.handleChange = this.handleChange.bind(this);
    this.handlePrevPreview = this.handlePrevPreview.bind(this);
    this.handleNextPreview = this.handleNextPreview.bind(this);
    this.handleComfirmUpload = this.handleComfirmUpload.bind(this);
    this.isObjectExisted = this.isObjectExisted.bind(this);
    this.loadClassify = this.loadClassify.bind(this);
  }

  loadClassify() {
    fetch(`/api/databases`, {
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
        completedFileList = this.state.completedFileList;

    fileList = fileList.filter((file) => {
      if (file.response && file.state !== 'done') {
        fetch(`/api/uploadcv/preview`, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Authorization': `Basic ${localStorage.token}`,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: file.response.data.id,
          }),
        })
        .then((response) => {
          return response.json();
        })
        .then((json) => {
          if (json.code === 200) {
            file.response.data = Object.assign(file.response.data, json.data);
            file.state = 'done';
            completedFileList.push(file.response.data);
            this.setState({
              completedFileList: completedFileList,
            });
          }
        });
        return file;
      }
      return true;
    });

    this.setState({
      fileList: fileList,
      comfirmResult: [],
    });
  }

  shouldComponentUpdate(nextProps, nextState) {
    return nextState.fileList.length === nextState.completedFileList.length;
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
    if (!this.isObjectExisted(comfirm, value.id)) {
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
    if (!this.isObjectExisted(comfirm, value.id)) {
      comfirm.push(value);
    }
    this.setState({
      currentPreview: current + 1,
      comfirmList: comfirm,
    });
  }

  handleComfirmUpload(value) {
    let comfirm = this.state.comfirmList;
    if (!this.isObjectExisted(comfirm, value.id)) {
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
      body: JSON.stringify({
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

  render() {
    const h = parseInt(document.body.offsetHeight) - 104;

    const uploadProps = {
      name: 'files',
      action: '/api/uploadcv',
      headers: {
        'Authorization': `Basic ${localStorage.token}`
      },
      multiple: false,
      onChange: this.handleChange,
    };

    return (
      <div>
        <Header />
        <div className="container" style={{ minHeight: h }}>
          <Uploader uploadProps={uploadProps} />
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
          {this.state.comfirmResult.length !== 0 ? <ComfirmResult comfirmResult={this.state.comfirmResult}/> : ''}
        </div>
        
      </div>
    );
  }
}