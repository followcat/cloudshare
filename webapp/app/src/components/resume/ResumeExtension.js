'use strict';
import React, { Component, PropTypes } from 'react';

import ResumeTag from './ResumeTag';

export default class ResumeExtension extends Component {

  constructor() {
    super();
  }

  render() {
    const tagList = this.props.dataSource.tag;
    return (
      <div className="resume-side">
        <ResumeTag dataSource={tagList} onSubmitTag={this.props.onSubmitTag}/>
      </div>
    );
  }
}

ResumeExtension.propTypes = {
  dataSource: PropTypes.shape({
    tag: PropTypes.array,
  }),
  onSubmitTag: PropTypes.func.isRequired,
};
