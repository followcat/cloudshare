'use strict';
import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import CVProcess from '../../utils/cv_process';

import './preview.less';

export default class Preview extends Component {

  constructor(props){
    super(props);
  }

  componentDidMount() {
    CVProcess.exec(ReactDOM.findDOMNode(this.refs.cv));
  }

  render() {
    return (
      <div>
        <div id="cv" ref="cv" dangerouslySetInnerHTML={{ __html: this.props.markdown }}></div>
      </div>
    );
  }
}