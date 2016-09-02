'use strict';
import React, { Component } from 'react';

import { Card } from 'antd';
import HistoryItem from './HistoryItem';

export default class BrowsingHistory extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Card title="Browsing History" bordered={true} bodyStyle={{ height: this.props.wrapperHeigth, overflowY: 'scroll' }}>
          {this.props.historyList.map((item) => {
              return <HistoryItem historyObject={item}/>
            })}
        </Card>
      </div>
    );
  }
}