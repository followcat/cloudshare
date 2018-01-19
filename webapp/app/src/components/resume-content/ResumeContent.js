'use strict';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';
import CVProcess from 'utils/cv-process';

import HighLight from 'components/highlight';

class ResumeContent extends Component {
  constructor() {
    super();
  }

  componentDidUpdate() {
    CVProcess.exec(ReactDOM.findDOMNode(this.refs.cv));
  }

  render() {
    const { highlight, html } = this.props;
    return (
       <div className={`${this.props.prefixCls}-html`}>
        <HighLight highlight={highlight} html={html}>
         <div
           ref="cv"
           dangerouslySetInnerHTML={{ __html: this.props.html }}
         />
        </HighLight>
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
