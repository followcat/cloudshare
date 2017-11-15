'use strict';
import React, { Component, PropTypes } from 'react';

import {
  UploadPreview,
  PreviewTopBar,
  VersionPrompt
} from 'components/upload-preview';
import Summary from 'components/summary';

import { generateSummary } from 'utils/summary-generator';

class Preview extends Component {
  render() {
    const {
      completedList,
      currentPreview,
      origins,
    } = this.props;
    return (
      <div>
        {completedList.map((item, index) => {
          return (
            <UploadPreview
              key={item.yaml_info.id}
              index={index}
              currentPreview={currentPreview}
              html={item.markdown || item.html}
            >
              <PreviewTopBar
                {...this.props}
                id={item.filename}  // id是标记文件唯一的标准,这里用filename作为辨识
                resumeID={item.yaml_info.id}
                name={item.yaml_info.name}
                origins={origins}
                classifyValue={item.yaml_info.classify}
                prevText="上一个"
                nextText="下一个"
                btnText="确认上传"
              />
              <VersionPrompt
                title="注意"
                message="简历库中可能存在相似的简历版本"
                dataSource={item.cv}
              />
              <Summary dataSource={generateSummary(item.yaml_info)} />
            </UploadPreview>
          );
        })}
      </div>
    );
  }
}

Preview.propTypes = {
  completedList: PropTypes.array,
  currentPreview: PropTypes.number,
};

export default Preview;
