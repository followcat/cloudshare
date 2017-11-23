'use strict';
import React, { Component, PropTypes } from 'react';

import ConfirmResult from 'components/confirm-result';

import { URL } from 'URL';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class UploaderResult extends Component {
  constructor() {
    super();
    this.getColumns = this.getColumns.bind(this);
    this.getConfirmResultRender = this.getConfirmResultRender.bind(this);
  }

  getColumns() {
    const columns = [{
      title: '文件名',
      dataIndex: 'filename',
      key: 'filename',
    }, {
      title: '上传状态',
      dataIndex: 'status',
      key: 'status',
      render: (text) => (
        text === 'success' ?
            <span style={{ color: 'green' }}>{language.SUCCESS}</span> :
            <span style={{ color: 'red' }}>{language.FAIL}</span>
      )
    }, {
      title: '信息',
      dataIndex: 'message',
      key: 'message',
      render: (text) => {switch(text){
        case "200": return (<span>{language.UPLOAD_SUCCESS}</span> );
        case "201": return (<span>{language.UPLOAD_EXISTED_PROJECTS}</span> );
        case "202": return (<span>{language.UPLOAD_EXISTED_PROJECT}</span> );
        case "203": return (<span>{language.UPLOAD_NO_CONTACT}</span> );
      }}
    }, {
      title: '操作',
      key: 'operation',
      render: (record) => {
        return (
          <a
            href={URL.getResumeURL(record.id)}
            target="_blank"
            disabled={record.status !== 'success' ? true : false}
          >
            打开简历
          </a>
        );
      }
    }];

    return columns;
  }

  getConfirmResultRender() {
    const {
      failedList,
      fileList,
      confirmResult
    } = this.props;

    const columns = this.getColumns();

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
      );
    } else {
      return null;
    }
  }

  render() {
    return (
      <div className="cs-uploader-result">
        {this.getConfirmResultRender()}
      </div>
    );
  }
}

UploaderResult.default = {
  fileList: [],
  failedList: [],
  confirmResult: []
};

UploaderResult.propTypes = {
  fileList: PropTypes.array,
  failedList: PropTypes.array,
  confirmResult: PropTypes.array
};

export default UploaderResult;
