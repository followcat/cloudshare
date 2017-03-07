'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Competency,
  Experience,
  Position
} from 'components/analyse-charts';

class ResultInfo extends Component {

  render() {
    const { total, keyword, dataSource } = this.props;

    const btnStyle = {
      display: 'inline-block',
      marginLeft: 4,
    };

    return (
      <div className="top-container">
        <div className="left-wrap">
          <p>有 <em>{total}</em> 条搜索结果</p>
          <p>关键词: <strong>{keyword}</strong></p>
        </div>
        <div className="right-wrap">
          <div><p style={{ fontWeight: 'bold' }}>分析工具:</p></div>
          <Position 
            style={btnStyle}
            keyword={this.props.keyword}
          />
          <Competency
            style={btnStyle}
            dataSource={dataSource}
          />
          <Experience
            style={btnStyle}
            dataSource={dataSource}
          />
        </div>
      </div>
    );
  }
}

ResultInfo.propTypes = {
  total: PropTypes.number,
  keyword: PropTypes.string,
  dataSource: PropTypes.array
};

export default ResultInfo;
