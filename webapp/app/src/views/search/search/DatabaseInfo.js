'use strict';
'use strict';
import React, { Component } from 'react';

import { getDatabaseInfo } from 'request/search';

import StorageUtil from 'utils/storage';

class DatabaseInfo extends Component {

  constructor() {
    super();
    this.state = {
      dbList: [],
      visible: false,
    };
    this.loadDatabaseInfo = this.loadDatabaseInfo.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.renderList = this.renderList.bind(this);
  }

  loadDatabaseInfo() {
    getDatabaseInfo((json) => {
      if (json.code === 200) {
        this.setState({
          dbList: json.data,
        });
      }
    });
  }

  handleClick() {
    if (this.state.visible) {
      this.setState({
        visible: false,
      });
    } else {
      this.setState({
        visible: true,
      });
    }
  }

  renderList() {
    const dbList = this.state.dbList,
          project = StorageUtil.get('_pj'),
          arr = [];
    for (let key in dbList) {
      if (key === project) {
        arr.unshift(<li key={key}>{`${key}: ${dbList[key]}`}</li>);
      } else {
        arr.push(<li key={key}>{`${key}: ${dbList[key]}`}</li>);
      }
    }
    return arr;
  }

  componentDidMount() {
    this.loadDatabaseInfo();
  }

  render() {
    const listClass = this.state.visible ? 'count-list showed' : 'count-list hidden',
          totalClass = this.state.visible ? 'total' : 'total radius';
    return (
      <div className="count-box">
        <ul className={listClass}>
          {this.renderList()}
        </ul>
        <div
          className={totalClass}
          onClick={this.handleClick}
        >
          {`总数量: ${this.state.dbList['total']}`}
        </div>
      </div>
    );
  }
}

export default DatabaseInfo;
