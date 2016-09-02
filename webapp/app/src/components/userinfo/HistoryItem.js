'use strict';
import React, { Component } from 'react';

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
    console.log(this.props.historyObject);
    return (
      <div>
        <div style={itemWrapStyle}>
          <span style={timeStyle}>{this.props.historyObject.time}</span>
          <a>{this.props.historyObject.name !== "" ? this.props.historyObject.name : this.props.historyObject.id}</a>
        </div>
      </div>
    );
  }
}