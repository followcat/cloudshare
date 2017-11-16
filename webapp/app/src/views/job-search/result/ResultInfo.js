'use strict';
import React, { Component, PropTypes } from 'react';
import { Button, Icon } from 'antd';

import { FilterForm } from 'components/filter-card';

import { API } from 'API';

import StorageUtil from 'utils/storage';

class ResultInfo extends Component {
  constructor() {
    super();
    this.state = {
      selected: { 'origin' : '其他' }
    }
  }
  render() {
    const { total, keyword, dataSource, industry } = this.props;
    const props = {
      name: 'files',
      action: API.UPLOAD_RESUME_API,
      data: this.state.selected,
      headers: {
        'Authorization': `Basic ${StorageUtil.get('token')}`
      },
      // onRemove: this.handleRemove,
    };
    
    return (
      <div className="top-container">
        <div className="left-wrap">
          <p>有 <em>{total}</em> 条搜索结果</p>
          <p>关键词: <strong>{keyword}</strong></p>
        </div>
        <div className="right-wrap">
          <div><p style={{ fontWeight: 'bold' }}>简历分析:</p></div>
        </div>
      </div>
    );
  }
}

ResultInfo.propTypes = {
  total: PropTypes.number,
  keyword: PropTypes.string,
  dataSource: PropTypes.array,
  industry: PropTypes.object,
  onFilter: PropTypes.func
};

export default ResultInfo;
