'use strict';
import React, { Component, PropTypes } from 'react';
import ReactDOM from 'react-dom';

import CVProcess from '../../utils/cv_process';

import './cvcontent.less';

export default class ResumeContent extends Component {

  componentDidUpdate() {
    CVProcess.exec(ReactDOM.findDOMNode(this.refs.cv));
  }

  render() {
    return (
      <div id="cv" ref="cv" dangerouslySetInnerHTML={{ __html: this.props.html }}></div>
    );
  }
}

ResumeContent.propTypes = {
  html: PropTypes.string,
};