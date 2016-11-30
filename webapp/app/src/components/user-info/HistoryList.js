'use strict';
import React, { Component, PropTypes } from 'react';
import { Card } from 'antd';

class HistoryList extends Component {
  render() {
    return (
      <div className="cs-history">
        {this.props.children}
      </div>
    );
  }
}

export default HistoryList;
