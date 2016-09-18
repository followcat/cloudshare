'use strict';
import React, { Component, PropTypes } from 'react';

export default class HistoryItem extends Component {
  render() {
    const itemWrapStyle = {
      borderBottomWidth: 1,
      borderBottomStyle: 'dashed',
      borderBottomColor: '#ececec',
      paddingTop: 8,
      paddingBottom: 8,
    };
    const timeStyle = {
      color: '#999',
      marginRight: 40,
    };

    return (
      <div>
        <div style={itemWrapStyle}>
          <span style={timeStyle}>{this.props.historyObject.time}</span>
          <a href={`/show/${this.props.historyObject.filename}`} target="_blank">{this.props.historyObject.name !== "" ? this.props.historyObject.name : this.props.historyObject.id}</a>
        </div>
      </div>
    );
  }
}

HistoryItem.propTypes = {
  historyObject: PropTypes.object,
};