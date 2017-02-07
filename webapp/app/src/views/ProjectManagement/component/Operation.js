'use strict';
import React, { Component, PropTypes } from 'react';

import { Checkbox } from 'antd';

import { URL } from '../../../config/url';

import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;

class Operation extends Component {
  constructor() {
    super();
    this.state = {
      appendCommentary: true
    };
    this.handleAppendCommentary = this.handleAppendCommentary.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  handleAppendCommentary() {
    this.setState({
      appendCommentary: !this.state.appendCommentary
    });
  }

  handleClick(e) {
    e.preventDefault();
    this.props.onEdit(this.props.record);
  }

  render() {
    return (
      <ul>
        <li><Checkbox defaultChecked={true} onChange={this.handleAppendCommentary}>{language.APPEND_COMMENTARY}</Checkbox></li>
        <li><a href={URL.getFastMatching(this.props.record.id, this.state.appendCommentary)}>{language.MATCH_ACTION}</a></li>
        <li><a onClick={this.handleClick}>{language.EDIT}</a></li>
      </ul>
    );
  }
}

Operation.propTypes = {

}

export default Operation;
