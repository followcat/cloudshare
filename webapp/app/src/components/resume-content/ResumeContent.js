'use strict';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';
import CVProcess from 'utils/cv-process';

class ResumeContent extends Component {
  constructor() {
    super();
  }

  componentDidUpdate() {
    CVProcess.exec(ReactDOM.findDOMNode(this.refs.cv));
  }

  render() {
    return (
      <div className={`${this.props.prefixCls}-wrapper`}>
        <div
          className={`${this.props.prefixCls}`}
          ref="cv"
          dangerouslySetInnerHTML={{ __html: this.props.html }}
        />
      </div>
    );
  }
}

ResumeContent.defaultProps = {
  prefixCls: 'cs-resume',
  html: '',
};

ResumeContent.propTypes = {
  prefixCls: PropTypes.string,
  html: PropTypes.string,
};

export default ResumeContent;
