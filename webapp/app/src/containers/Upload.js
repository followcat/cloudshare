'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import Header from '../components/common/Header';
import Uploader from '../components/upload/Uploader';

import './upload.less';

export default class Upload extends Component {

  constructor(props) {
    super(props);
    this.state = {
      fileList: [],
      completedFileList: []
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(info) {
    let fileList = info.fileList,
        completedFileList = this.state.completedFileList;

    fileList.map((file) => {
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
            completedFileList.push(file);
          }
        });

        this.setState({
          completedFileList: completedFileList,
        });
      }
    });
  }

  render() {
    const h = parseInt(document.body.offsetHeight) - 104;

    const uploadProps = {
      name: 'files',
      action: '/api/uploadcv',
      headers: {
        'Authorization': `Basic ${localStorage.token}`
      },
      mutiple: true,
      onChange: this.handleChange,
    };

    return (
      <div>
        <Header />
        <div className="container" style={{ minHeight: h }}>
          <Uploader uploadProps={uploadProps} />
        </div>
      </div>
    );
  }
}