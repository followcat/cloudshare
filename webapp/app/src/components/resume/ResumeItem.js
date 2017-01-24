'use strict';
import React, { Component, PropTypes } from 'react';
import ResumeWrapper from './ResumeWrapper';
import { Spin } from 'antd';

class ResumeItem extends Component {
  constructor(props) {
    super(props);
  }

  shouldComponentUpdate(nextProps, nextState) {
    if (nextProps.id === this.props.id) {
      return true;
    }
    return false;
  }

  render() {
    const props = this.props;
    return (
      <Spin spinning={props.paneLoading}>
        <ResumeWrapper 
          dataSource={props.dataSource}
          summary={props.summary}
          html={props.html}
          enHtml={props.enHtml}
          collected={props.collected}
          upload={props.upload}
          fileList={props.fileList}
          jdList={props.jdList}
          radarOption={props.radarOption}
          chartSpinning={props.chartSpinning}
          enComfirmLoading={props.enComfirmLoading}
          onModifyTitle={props.onModifyTitle}
          onCollection={props.onCollection}
          onEnComfirmLoading={props.onEnComfirmLoading}
          onDrawChartOpen={props.onDrawChartOpen}
          onDrawChartSubmit={props.onDrawChartSubmit}
          onDownloadClick={props.onDownloadClick}
        />
      </Spin>
    );
  }
}

ResumeItem.propTypes = {
  id: PropTypes.string,
};

export default ResumeItem;
