'use strict';
import React, { Component, PropTypes } from 'react';

import { Card } from 'antd';
import HistoryItem from './HistoryItem';

export default class BrowsingHistory extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Card title="Browsing History" bordered={true} bodyStyle={{ height: this.props.historyHeight, overflowY: 'scroll' }}>
          {this.props.historyList.map((item, index) => {
              return <HistoryItem key={index} historyObject={item}/>
            })}
        </Card>
      </div>
    );
  }
}

BrowsingHistory.propTypes = {
  historyList: PropTypes.array,
  historyHeight: PropTypes.number,
};