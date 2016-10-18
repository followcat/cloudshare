'use strict';
import React, { Component } from 'react';

import { Icon } from 'antd';

import './Tag.less';

export default class Tag extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="cs-tag">
        <span className="cs-tag-text">{this.props.text}</span>
        <Icon type="cross-circle-o" onClick={this.props.onClick} />
      </div>
    );
  }
}