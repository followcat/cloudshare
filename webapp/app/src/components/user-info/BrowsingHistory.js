'use strict';
import React, { Component, PropTypes } from 'react';
import HistoryList from './HistoryList';
import HistoryItem from './HistoryItem';
import { Card } from 'antd';


class BrowsingHistory extends Component {
  render() {
    const props = this.props;

    return (
      <Card
        title={props.title}
        bordered={props.bordered}
        bodyStyle={props.bodyStyle}
      >
        <HistoryList>
          {props.storage.map((item, index) => {
            return (
              <HistoryItem
                {...item}
                key={index}
              />
            );
          })}
        </HistoryList>
      </Card>
    );
  }
}

BrowsingHistory.defaultProps = {
  title: 'Browsing History',
  storage: [],
  bordered: true,
};

BrowsingHistory.propTypes = {
  storage: PropTypes.array,
  bordered: PropTypes.bool,
  bodyStyle: PropTypes.object,
};

export default BrowsingHistory;
