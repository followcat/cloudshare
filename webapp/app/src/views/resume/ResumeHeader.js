'use strict';
import React, { Component, PropTypes } from 'react';

import { Icon } from 'antd';

import { getSourceURL } from 'utils/source';

class ResumeHeader extends Component {
  render() {
    const { collected, dataSource } = this.props;

    return (
      <div className="cs-resume-header">
        <div className="collect">
          <Icon
            type={collected ? 'star' : 'star-o'}
            style={collected ? { color: '#FFC107' } : {}}
            onClick={this.props.onCollection}
          />
        </div>
        <div className="cs-resume-header-info">
          <label>简历ID: </label>
          <span>{dataSource.id}</span>
        </div>
        <div className="cs-resume-header-info">
          <label>上传人: </label>
          <span>{`${dataSource.committer}, ${dataSource.date && dataSource.date.split(' ')[0]}`}</span>
        </div>
      </div>
    );
  }
}

ResumeHeader.propTypes = {
  collected: PropTypes.bool,
  dataSource: PropTypes.object,
  onCollection: PropTypes.func
};

export default ResumeHeader;
