'use strict';
import React, { Component, PropTypes } from 'react';

import ResumeTag from './ResumeTag';
import ResumeFollowUp from './ResumeFollowUp';
import ResumeComment from './ResumeComment';
import ResumeSimilar from './ResumeSimilar';

export default class ResumeExtension extends Component {
  render() {
    const tagList = this.props.dataSource.tag,
          followUpList = this.props.dataSource.tracking,
          commentList = this.props.dataSource.comment,
          similarList = this.props.similar;

    return (
      <div className="resume-side">
        <ResumeTag dataSource={tagList} onSubmitTag={this.props.onSubmitTag}/>
        <ResumeFollowUp dataSource={followUpList} onSubmitFollowUp={this.props.onSubmitFollowUp}/>
        <ResumeComment dataSource={commentList} onSubmitComment={this.props.onSubmitComment}/>
        <ResumeSimilar dataSource={similarList}/>
      </div>
    );
  }
}

ResumeExtension.propTypes = {
  dataSource: PropTypes.shape({
    tag: PropTypes.array,
    tracking: PropTypes.array,
    comment: PropTypes.array,
  }),
  onSubmitTag: PropTypes.func,
  onSubmitFollowUp: PropTypes.func,
  onSubmitComment: PropTypes.func,
};
